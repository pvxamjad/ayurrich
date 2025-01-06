from django.conf import settings
from django.core.mail import send_mail
import logging

logger = logging.getLogger(__name__)

def send_order_email(order_summary):
    """
    Sends an email notification to the admin.
    """
    try:
        subject = f"New Order Received - {order_summary.order_id}"
        
        # Initialize the products string
        products_info = ""
        
        # Loop through each product in the order
        for product in order_summary.order_products:
            products_info += (
                f"Product: {product['product']}\n"
                f"Quantity: {product['quantity']}\n"
                f"Price: ₹{product['price']}\n"
                f"Total Price: ₹{product['total_price']}\n\n"
            )

        # Construct the message with proper formatting
        message = (
            f"Order ID: {order_summary.order_id}\n"
            f"Total Amount: ₹{order_summary.total_amount}\n\n"
            f"Customer Name: {order_summary.shipping_info['full_name']}\n"
            f"Customer Email: {order_summary.shipping_info['email']}\n"
            f"Customer Address: {order_summary.shipping_info['address']}, "
            f"{order_summary.shipping_info['city']}, {order_summary.shipping_info['state']}, "
            f"{order_summary.shipping_info['pincode']}, {order_summary.shipping_info['country']}\n\n"
            f"Ordered Products:\n"
            f"{products_info}"
        )
        
        recipient_list = [order_summary.shipping_info['email']]
        sender_email = 'amjadpvamd@gmail.com'  # Replace with the sender's email

        send_mail(
            subject,
            message,
            sender_email,
            recipient_list,
            fail_silently=False,  # Set to False to see errors
        )
        
        logger.info("Order email sent successfully!")
    except Exception as e:
        logger.error("Error sending order email: %s", str(e))

