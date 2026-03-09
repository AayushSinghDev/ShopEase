def get_low_stock_products(seller=None):
    """
    Stock <= LOW_STOCK_THRESHOLD wale products return karo.
    Agar seller diya toh sirf us seller ke products.
    """
    from products.models import Product, LOW_STOCK_THRESHOLD
    qs = Product.objects.filter(stock__lte=LOW_STOCK_THRESHOLD)
    if seller:
        qs = qs.filter(seller=seller)
    return qs.select_related('category', 'seller').order_by('stock')


def send_low_stock_alert_email(product):
    """Seller ko email bhejo jab product ka stock low ho jaye."""
    from django.core.mail import send_mail
    from django.conf import settings
    try:
        send_mail(
            subject=f"⚠️ Low Stock Alert: {product.name}",
            message=(
                f"Dear {product.seller.name},\n\n"
                f"Your product '{product.name}' has only {product.stock} unit(s) left in stock.\n"
                f"Please restock soon to avoid missing orders.\n\n"
                f"Seller Panel: http://127.0.0.1:8000/seller/products/\n\n"
                f"— ShopEase Team"
            ),
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[product.seller.email],
            fail_silently=True,
        )
    except Exception:
        pass
