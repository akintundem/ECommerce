import json
from datetime import datetime


class Cart:
    def __init__(self):
        pass

    def add_product(self, product_id, quantity, user_id, cursor, conn):
        if add_to_cart(product_id, quantity, user_id, cursor, conn):
            return "Added to cart"
        else:
            return "Unable to add to cart"

    def remove_product(self, product_id, user_id, cursor, conn):
        if remove_from_cart(product_id, user_id, cursor, conn):
            return "Removed from cart"
        else:
            return "Unable to remove from cart"

    def update_quantity(self, product_id, new_quantity, user_id, cursor, conn):
        if update_cart_item_quantity(product_id, new_quantity, user_id, cursor, conn):
            return "Quantity updated"
        else:
            return "Unable to update quantity"

    def empty_cart(self, user_id, cursor, conn):
        if empty_cart(user_id, cursor, conn):
            return "Cart emptied"
        else:
            return "Unable to empty cart"
    
    def view_cart(self, request_message, cursor,conn):
        cart_items = view_cart_query(request_message, cursor)
        if cart_items:
            return json.dumps(cart_items)
        else:
            return "Cart is empty"
    
    def add_shipping_address(self, request_message, cursor,conn):
        if shipping_query(request_message, cursor, conn):
            return "Shipping address added"
        else:
            return "Unable to add shipping address"
    def place_order(self, request_message, cursor,conn):
        if place_order_query(request_message, cursor, conn):
            return "Order placed"
        else:
            return "Unable to place order"
        
def shipping_query(shipping_address,cursor):
    query = '''
        INSERT INTO ShippingAddress (user_id, shipping_address)
        VALUES (?, ?)
    '''
    cursor.execute(query, (shipping_address['user_id'], shipping_address['shipping_address']))
    return True

def place_order_query(order,cursor):
    query = '''
        INSERT INTO Orders (user_id, order_date, total_price, shipping_address)
        VALUES (?, ?, ?, ?)
    '''
    cursor.execute(query, (order['user_id'], order['order_date'], order['total_price'], order['shipping_address']))
    return True

def view_cart_query(user_id, cursor):
    try:
        # Retrieve the cart_id associated with the user
        cursor.execute("SELECT cart_id FROM UserCart WHERE user_id = ?", (user_id,))
        cart_id = cursor.fetchone()

        if cart_id is None:
            # User doesn't have a cart, return an empty list
            return []

        cart_id = cart_id[0]  # Extract cart_id from the result

        # Retrieve all products in the user's cart
        cursor.execute("SELECT product_id, quantity FROM ShoppingCart WHERE cart_id = ?", (cart_id,))
        cart_items = cursor.fetchall()

        products = []
        for item in cart_items:
            product_id, quantity = item
            # Fetch product details based on product_id
            cursor.execute("SELECT * FROM Products WHERE product_id = ?", (product_id,))
            product_details = cursor.fetchone()
            if product_details:
                product = {
                    'product_id': product_id,
                    'product_name': product_details[1],
                    'discounted_price': float(product_details[2]),
                    'actual_price': float(product_details[3]),
                    'discount_percentage': float(product_details[4]),
                    'rating': float(product_details[5]),
                    'rating_count': int(product_details[6]),
                    'about_product': product_details[7],
                    'number_of_inventory': int(product_details[8]),
                    'img_link': product_details[9],
                    'quantity': quantity
                }
                products.append(product)

        return products
    except Exception as e:
        # Handle any errors
        print("Error:", e)
        return []



def add_to_cart(product_id, quantity, user_id, cursor, conn):
    try:
        # Begin a transaction
        cursor.execute("BEGIN TRANSACTION")
        
        created_at = datetime.now()

        # Execute INSERT query
        query_insert = '''INSERT INTO Users (username, password, email, full_name, address, phone_number, created_at)
                        VALUES (?, ?, ?, ?, ?, ?, ?)
                    '''
        cursor.execute(query_insert, ("akintundemayokun@gmail.com", "Iamayokakfwesh1", "akintundemayokun@gmail.com", "Mayokun Moses Akintunde", "63 Lark Ridge", "080213232", created_at))

        # Check if the user has a cart
        cursor.execute("SELECT cart_id FROM UserCart WHERE user_id = ?", (user_id,))
        cart_id = cursor.fetchone()
        
        if cart_id is None:
            # If the user doesn't have a cart, create a new cart entry
            cursor.execute(
                "INSERT INTO UserCart (user_id) OUTPUT INSERTED.cart_id VALUES (?)",
                (user_id,)
            )
            cart_id = cursor.fetchone()[0]    
        else:
            cart_id = cart_id[0]  # Extract cart_id from the result
        
        # Insert the item into the shopping cart
        cursor.execute("INSERT INTO ShoppingCart (cart_id, product_id, quantity) VALUES (?, ?, ?)", (cart_id, product_id, quantity))
        
        # Commit the transaction
        conn.commit()
        
        return True
    except Exception as e:
        print("Error:", e)
        conn.rollback()  # Rollback the transaction in case of an error
        return False
    
def remove_from_cart(product_id, user_id, cursor, conn):
    try:
        # Begin a transaction
        cursor.execute("BEGIN TRANSACTION")

        # Get the cart_id associated with the user
        cursor.execute("SELECT cart_id FROM UserCart WHERE user_id = ?", (user_id,))
        cart_id = cursor.fetchone()

        if cart_id is None:
            # User doesn't have a cart, no action needed
            return False

        cart_id = cart_id[0]  # Extract cart_id from the result

        # Remove the item from the shopping cart
        cursor.execute("DELETE FROM ShoppingCart WHERE cart_id = ? AND product_id = ?", (cart_id, product_id))

        # Check if the user has any remaining items in the cart
        cursor.execute("SELECT COUNT(*) FROM ShoppingCart WHERE cart_id = ?", (cart_id,))
        remaining_items_count = cursor.fetchone()[0]

        if remaining_items_count == 0:
            # If the user has no remaining items, delete the cart entry from UserCart
            cursor.execute("DELETE FROM UserCart WHERE cart_id = ?", (cart_id,))

        # Commit the transaction
        conn.commit()

        return True
    except Exception as e:
        conn.rollback()  # Rollback the transaction in case of an error
        return False

def update_cart_item_quantity(product_id, new_quantity, user_id, cursor, conn):
    try:
        # Begin a transaction
        cursor.execute("BEGIN TRANSACTION")

        # Get the cart_id associated with the user
        cursor.execute("SELECT cart_id FROM UserCart WHERE user_id = ?", (user_id,))
        cart_id = cursor.fetchone()

        if cart_id is None:
            # User doesn't have a cart, no action needed
            return False

        cart_id = cart_id[0]  # Extract cart_id from the result

        # Update the quantity of the item in the shopping cart
        cursor.execute("UPDATE ShoppingCart SET quantity = ? WHERE cart_id = ? AND product_id = ?", (new_quantity, cart_id, product_id))

        # Commit the transaction
        conn.commit()

        return True
    except Exception as e:
        conn.rollback()  # Rollback the transaction in case of an error
        return False

def empty_cart(user_id, cursor, conn):
    try:
        # Begin a transaction
        cursor.execute("BEGIN TRANSACTION")

        # Get the cart_id associated with the user
        cursor.execute("SELECT cart_id FROM UserCart WHERE user_id = ?", (user_id,))
        cart_id = cursor.fetchone()

        if cart_id is None:
            # User doesn't have a cart, no action needed
            return False

        cart_id = cart_id[0]  # Extract cart_id from the result

        # Delete all items from the shopping cart associated with the user's cart
        cursor.execute("DELETE FROM ShoppingCart WHERE cart_id = ?", (cart_id,))

        # Remove the cart entry from the UserCart table
        cursor.execute("DELETE FROM UserCart WHERE cart_id = ?", (cart_id,))

        # Commit the transaction
        conn.commit()

        return True
    except Exception as e:
        conn.rollback()  # Rollback the transaction in case of an error
        return False
