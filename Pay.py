class PaymentHandler:
    def __init__(self):
        pass
    
    def process_payment(self, amount, card_number, card_expiry, card_cvv):
        # Implement payment processing logic here
        # Use self.payment_gateway to interact with the payment gateway API
        # Return True if payment is successful, False otherwise
        pass

    def refund_payment(self, transaction_id, amount):
        # Implement refund logic here
        # Use self.payment_gateway to interact with the payment gateway API
        # Return True if refund is successful, False otherwise
        pass