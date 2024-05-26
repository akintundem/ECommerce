import json
from VerifyToken import TokenVerifier
from Recommendation.Recommend import Recommendation
from Search.SearchEngine import Search
from Cart.Cart import Cart
from Pay import PaymentHandler
from flask import Flask, request
from db.db import DatabaseManager
app = Flask(__name__)



VerifyUser = TokenVerifier("S", "A")

config_file = 'db/db_cred.json' 
datab = DatabaseManager(config_file)
db = datab.get_cursor()
conn = datab.get_connection()

recommendation = Recommendation()
search = Search()
cart = Cart()
pay = PaymentHandler()

@app.route('/recommend', methods=['GET'])
def recommend():
    token = request.headers.get('Token')
    if VerifyUser.verify_tokens(token):
        response = recommendation.get_recommendations(db)
        if response:
            return json.dumps({'message': response})
        else:
            response = "No recommendations"
            return json.dumps({'message': response})
    else:
        response = "Invalid token"
        return json.dumps({'message': response})

@app.route('/search', methods=['POST'])
def searchProd():
    token = request.headers.get('Token')
    params = request.args.get('search')
    if VerifyUser.verify_tokens(token):
        response = search.search_products(params,db)
        if response:
            return json.dumps({'message': response})
        else:
            response = "None"
            return json.dumps({'message': response})
    else:
        response = "Invalid token"
        return json.dumps({'message': response})
@app.route('/cart', methods=['GET'])
def cartView():
    token = request.headers.get('Token')
    if VerifyUser.verify_tokens(token):
        userID = 1
        response = cart.view_cart(userID,db)
        if response:
            return json.dumps({'message': response})
        else:
            response = "None"
            return json.dumps({'message': response})
    else:
        response = "Invalid token"
        return json.dumps({'message': response})
    
@app.route('/cart', methods=['POST'])
def cartActions():
    token = request.headers.get('Token')
    data = json.loads(request.data.decode('utf-8'))
    
    if VerifyUser.verify_tokens(token):
        action = data.get('action')
        userID = 1
        # Handle different actions
        # Add: Add a product to the cart{
        # "action": "add",
        # "product_id": "B097JVLW3L",
        # "quantity": 1
        # }
        if action == 'add':
            product_id = data.get('product_id')
            quantity = data.get('quantity')
            response = cart.add_product(product_id, quantity, 1, db, conn)
        # Remove: Remove a product from the cart{
        # "action": "remove",
        # "product_id": "123"
        # }
        elif action == 'remove':
            product_id = data.get('product_id')
            response = cart.remove_product(product_id, 1, db, conn)
        # Update Quantity: Update the quantity of a product in the cart{
        # "action": "update_quantity",
        # "product_id": "123",
        # "quantity": 2
        # }
        elif action == 'update_quantity':
            product_id = data.get('product_id')
            quantity = data.get('quantity')
            response = cart.update_quantity(product_id, quantity, userID, db, conn)
        # empty: Empty the cart{
        #   "action": "empty"
        # }
        elif action == 'empty':
            response = cart.empty_cart(userID, db, conn)
        else:
            response = "Invalid action"
        
        # Return response
        return json.dumps({'message': response})
    else:
        response = "Invalid token"
        return json.dumps({'message': response})


@app.route('/product_detail', methods=['GET'])
def product():
    data = json.loads(request.data)
    token = data.get('Token')
    if VerifyUser.verify_tokens(token):
        request_message = data.get('message')
        response = search.detail_product(request_message,db)
        if response:
            return json.dumps({'message': response})
        else:
            response = "None"
            return json.dumps({'message': response})
    else:
        response = "Invalid token"
        return json.dumps({'message': response})
        
            
@app.route('/delete_from_cart', methods=['POST'])
def deleteCart():
    data = json.loads(request.data)
    token = data.get('Token')
    if VerifyUser.verify_tokens(token):
        request_message = data.get('message')
        response = cart.remove_product(request_message,db) 
        if response:
            return json.dumps({'message': response})
        else:
            response = "None"
            return json.dumps({'message': response})
    else:
        response = "Invalid token"
        return json.dumps({'message': response})

@app.route('/checkout', methods=['POST'])
def getUserCart():
    data = json.loads(request.data)
    token = data.get('Token')
    if VerifyUser.verify_tokens(token):
        request_message = data.get('message')
        response = cart.get_user_products(request_message,db)
        if response:
            return json.dumps({'message': response})
        else:
            response = "None"
            return json.dumps({'message': response})
    else:
        response = "Invalid token"
        return json.dumps({'message': response})


@app.route('/pay', methods=['POST'])
def pay():
    data = json.loads(request.data).get('Token')
    token = data
    if VerifyUser.verify_tokens(token):
        request_message = data.get('message')
        response = pay.process_payment(request_message,db)
        if response:
            return json.dumps({'message': response})
        else:
            response = "None"
            return json.dumps({'message': response})
    else:
        response = "Invalid token"
        return json.dumps({'message': response})

if __name__ == '__main__':
    app.run(port=8888)