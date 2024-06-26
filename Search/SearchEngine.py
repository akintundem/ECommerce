import json
class Search:
    def __init__(self):
        pass

    def search_products(self, query, cursor):
        results = None
        try:
            results = search_query(query,cursor)
        except Exception as e:
            return None
        return results
    
    def detail_product(self, query, cursor):
        results = None
        try:
            results = detail_query(query,cursor)
        except Exception as e:
            return None
        return results

def detail_query(product_id,cursor):
    query = '''
        SELECT p.product_id, p.product_name, p.discounted_price, p.actual_price, p.discount_percentage, p.rating, p.rating_count, p.about_product, p.number_of_inventory, p.img_link
        FROM Products p
        WHERE p.product_id = ?
    '''
    cursor.execute(query, (product_id,))
    rows = cursor.fetchall()
    products = []
    for row in rows:
        product = {
            'product_id': row[0],
            'product_name': row[1],
            'discounted_price': float(row[2]),
            'actual_price': float(row[3]),
            'discount_percentage': float(row[4]),
            'rating': float(row[5]),
            'rating_count': int(row[6]),
            'about_product': row[7],
            'number_of_inventory': int(row[8]),
            'img_link': row[9]
        }
        products.append(product)
    return json.dumps(products)


def search_query(search_name,cursor):
    query = '''
        SELECT p.product_id, p.product_name, p.discounted_price, p.actual_price, p.discount_percentage, p.rating, p.rating_count, p.about_product, p.number_of_inventory, p.img_link
        FROM Products p
        INNER JOIN ProductCategories pc ON p.product_id = pc.product_id
        INNER JOIN Categories c ON pc.category_id = c.category_id
        WHERE c.name = ? OR p.product_name = ? OR p.product_id = ?
    '''
    cursor.execute(query, (search_name, search_name, search_name))
    rows = cursor.fetchall()
    products = []
    for row in rows:
        product = {
            'product_id': row[0],
            'product_name': row[1],
            'discounted_price': float(row[2]),
            'actual_price': float(row[3]),
            'discount_percentage': float(row[4]),
            'rating': float(row[5]),
            'rating_count': int(row[6]),
            'about_product': row[7],
            'number_of_inventory': int(row[8]),
            'img_link': row[9]
        }
        products.append(product)
    return json.dumps(products)
