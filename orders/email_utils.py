from django.core.mail import EmailMultiAlternatives, send_mail
from django.template.loader import render_to_string
from django.conf import settings


def send_order_confirmation_email(order):
    """Customer ko order confirmation email bhejo."""
    try:
        items = order.items.select_related('product')
        context = {'order': order, 'items': items}
        html_body = render_to_string('emails/order_confirmation.html', context)
        text_body = (
            f"Dear {order.customer.name},\n\n"
            f"Your Order #{order.pk} has been placed successfully!\n"
            f"Total: ₹{order.total}\n"
            f"Payment: {order.get_payment_method_display()}\n\n"
            f"Thank you for shopping with ShopEase!"
        )
        email = EmailMultiAlternatives(
            subject=f"Order #{order.pk} Confirmed — ShopEase",
            body=text_body,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[order.customer.email],
        )
        email.attach_alternative(html_body, "text/html")
        email.send(fail_silently=True)
    except Exception:
        pass  # Email fail hone pe order cancel mat ho


def send_order_status_update_email(order):
    """Customer ko order status update email bhejo."""
    try:
        items = order.items.select_related('product')
        context = {'order': order, 'items': items}
        html_body = render_to_string('emails/order_status_update.html', context)
        text_body = (
            f"Dear {order.customer.name},\n\n"
            f"Your Order #{order.pk} status has been updated to: {order.status.upper()}\n\n"
            f"Thank you for shopping with ShopEase!"
        )
        email = EmailMultiAlternatives(
            subject=f"Order #{order.pk} Status Update — {order.status.title()} | ShopEase",
            body=text_body,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[order.customer.email],
        )
        email.attach_alternative(html_body, "text/html")
        email.send(fail_silently=True)
    except Exception:
        pass


def send_seller_new_order_email(order):
    """
    Jab order place ho, har seller ko notify karo jinke products order mein hain.
    Ek seller ko ek hi email jaaye (agar multiple items same seller ke hain).
    """
    try:
        items = order.items.select_related('product__seller')

        # Sellers group karo
        seller_items = {}
        for item in items:
            seller = item.product.seller
            if seller not in seller_items:
                seller_items[seller] = []
            seller_items[seller].append(item)

        for seller, seller_order_items in seller_items.items():
            context = {
                'order': order,
                'seller': seller,
                'seller_items': seller_order_items,
            }
            html_body = render_to_string('emails/seller_new_order.html', context)
            text_body = (
                f"Dear {seller.name},\n\n"
                f"You have a new order! Order #{order.pk}\n"
                f"Items: {len(seller_order_items)}\n\n"
                f"Please check your seller dashboard.\n\nShopEase Team"
            )
            email = EmailMultiAlternatives(
                subject=f"New Order #{order.pk} Received — ShopEase Seller",
                body=text_body,
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[seller.email],
            )
            email.attach_alternative(html_body, "text/html")
            email.send(fail_silently=True)
    except Exception:
        pass
