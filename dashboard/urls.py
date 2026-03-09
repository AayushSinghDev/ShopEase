from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.admin_home, name='home'),

    # Customers
    path('customers/', views.manage_customers, name='customers'),
    path('customers/delete/<int:pk>/', views.delete_customer, name='delete_customer'),

    # Sellers
    path('sellers/', views.manage_sellers, name='sellers'),
    path('sellers/approve/<int:pk>/', views.approve_seller, name='approve_seller'),
    path('sellers/reject/<int:pk>/', views.reject_seller, name='reject_seller'),
    path('sellers/delete/<int:pk>/', views.delete_seller, name='delete_seller'),

    # Products
    path('products/', views.manage_products, name='products'),
    path('products/delete/<int:pk>/', views.delete_product, name='delete_product'),

    # Orders
    path('orders/', views.manage_orders, name='orders'),
    path('orders/update/<int:pk>/', views.update_order_status, name='update_order_status'),

    # Discounts
    path('discounts/', views.manage_discounts, name='discounts'),
    path('discounts/delete/<int:pk>/', views.delete_discount, name='delete_discount'),

    # Analytics
    path('analytics/', views.revenue_analytics, name='analytics'),

    # CSV Exports
    path('export/orders/', views.export_orders_csv, name='export_orders'),
    path('export/products/', views.export_products_csv, name='export_products'),
    path('export/customers/', views.export_customers_csv, name='export_customers'),

    # Banners
    path('banners/', views.manage_banners, name='banners'),
    path('banners/delete/<int:pk>/', views.delete_banner, name='delete_banner'),
]
