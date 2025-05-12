import stripe
import json
class PaymentHandler:
    def __init__(self, config_file):
        with open(config_file, 'r') as f:
            config = json.load(f)
        
        stripe.api_key = config["STRIPE_SECRET_KEY"]
        stripe.Account.create(
            type="express",
            capabilities={
                "card_payments": {"requested": True},
                "transfers": {"requested": True},
            },
        )
sdsd
    def create_payment_checkout_session(self, request_message):
        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[
                {
                    "price_data": {
                        "currency": "usd",
                        "product_data": {
                            "name": "Sample Item",
                        },
                        "unit_amount": 1000,  
                    },
                    "quantity": 1,
                }
            ],
            payment_intent_data={
                "application_fee_amount": 123, 
                "transfer_data": {
                    "destination": "{{CONNECTED_ACCOUNT_ID}}",  # optional connected account id
                },
            },
            mode="payment",
            success_url="https://example.com/success",
            cancel_url="https://example.com/cancel",
        )
        return session.id

