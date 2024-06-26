import stripe
import json
class PaymentHandler:
    def __init__(self, config_file):
        with open(config_file, 'r') as f:
            config = json.load(f)
        
        stripe.api_key = config["STRIPE_SECRET_KEY"]

    def create_payment_checkout_session(self, products):
        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[
                {
                    "price_data": {
                        "currency": "cad",
                        "product_data": {
                            "name": product['product_name'],
                        },
                        "unit_amount": int(product['actual_price'] * 100), 
                    },
                    "quantity": product['quantity'],
                } for product in products
            ],
            mode="payment",
            success_url="https://example.com/success",
            cancel_url="https://example.com/cancel",
        )

        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=products,
            mode="payment",
            success_url="https://example.com/success",
            cancel_url="https://example.com/cancel",
        )
        return session.id




# def main():
#     # Load configuration from a JSON file
#     config_file = "Payment/pay_cred.json"  # Update with your actual config file path
#     with open(config_file, 'r') as f:
#         config = json.load(f)
    
#     # Initialize PaymentHandler instance
#     payment_handler = PaymentHandler(config_file)
    
#     # Example: Create a payment checkout session
#     request_message = {
#         "customer_email": "test@example.com",
#         # Add other required fields as per your implementation
#     }
#     session_id = payment_handler.create_payment_checkout_session(request_message)
    
#     print(f"Created payment session with session ID: {session_id}")

# if __name__ == "__main__":
#     main()