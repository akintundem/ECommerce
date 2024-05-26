import json
from VerifyToken import TokenVerifier
from Recommendation.Recommend import Recommendation
from Search.SearchEngine import Search
from Cart import Cart
from Pay import PaymentHandler
from flask import Flask, request
from db.db import DatabaseManager
app = Flask(__name__)



VerifyUser = TokenVerifier("S", "A")

config_file = 'db/db_cred.json' 
datab = DatabaseManager(config_file)
db = datab.get_cursor()

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

@app.route('/search', methods=['GET'])
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
        
@app.route('/save_to_cart', methods=['POST'])
def saveCart():
    data = json.loads(request.data)
    token = data.get('Token')
    if VerifyUser.verify_tokens(token):
        request_message = data.get('message')
        response = cart.add_product(request_message,db) 
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