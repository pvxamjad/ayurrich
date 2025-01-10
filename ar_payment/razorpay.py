import razorpay
from django.conf import settings

class RazorpayClient:
    def __init__(self):
        self.client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

    def create_order(self, amount, currency="INR", payment_capture=1):
        """
        Create a Razorpay order.
        :param amount: Amount in paise (e.g., 50000 for ₹500)
        :param currency: Currency code, default is INR.
        :param payment_capture: 1 for automatic capture, 0 for manual.
        :return: The created order object.
        """
        payment_data = {
            "amount": amount,
            "currency": currency,
            "payment_capture": payment_capture,
        }
        return self.client.order.create(data=payment_data)

    def verify_signature(self, data):
        """
        Verify Razorpay payment signature.
        :param data: Dictionary containing 'razorpay_order_id', 'razorpay_payment_id', and 'razorpay_signature'.
        :return: None if the signature is valid, raises SignatureVerificationError otherwise.
        """
        return self.client.utility.verify_payment_signature(data)
