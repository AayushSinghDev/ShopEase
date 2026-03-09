from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    # Cart
    path('cart/', views.cart_view, name='cart'),
    path('cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/increase/<int:product_id>/', views.increase_quantity, name='increase_quantity'),
    path('cart/decrease/<int:product_id>/', views.decrease_quantity, name='decrease_quantity'),
    path('cart/remove/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('cart/clear/', views.clear_cart, name='clear_cart'),

    # Checkout
    path('checkout/', views.checkout, name='checkout'),
    path('place-order/', views.place_order, name='place_order'),
    path('razorpay-callback/', views.razorpay_callback, name='razorpay_callback'),

    # Orders
    path('confirmation/<int:pk>/', views.order_confirmation, name='confirmation'),
    path('my-orders/', views.order_list, name='order_list'),
    path('detail/<int:pk>/', views.order_detail, name='order_detail'),

    # Address
    path('address/add/', views.add_address, name='add_address'),
    path('address/delete/<int:pk>/', views.delete_address, name='delete_address'),

    # Invoice
    path('invoice/<int:pk>/', views.download_invoice, name='invoice'),
]
