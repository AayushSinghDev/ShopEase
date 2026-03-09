from django.urls import path
from . import views
from . import seller_views

app_name = 'accounts'

urlpatterns = [
    # Auth
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),

    # Dashboards
    path('dashboard/customer/', views.customer_dashboard, name='customer_dashboard'),
    path('dashboard/seller/', views.seller_dashboard, name='seller_dashboard'),
    path('dashboard/admin/', views.admin_dashboard, name='admin_dashboard'),

    path('my-account/', views.my_account, name='my_account'),

    # Facial Recognition — Customer & Seller only (no SuperAdmin)
    path('face-register/', views.face_register, name='face_register'),
    path('face-login/', views.face_login, name='face_login'),
]

# Seller panel URLs — separate prefix in main urls.py
seller_urlpatterns = [
    path('dashboard/', seller_views.seller_dashboard, name='seller_dashboard'),
    path('products/', seller_views.seller_products, name='seller_products'),
    path('product/add/', seller_views.add_product, name='add_product'),
    path('product/edit/<int:pk>/', seller_views.edit_product, name='edit_product'),
    path('product/delete/<int:pk>/', seller_views.delete_product, name='delete_product'),
    path('orders/', seller_views.seller_orders, name='seller_orders'),
    path('orders/update/<int:pk>/', seller_views.update_order_status, name='update_order_status'),
    path('discounts/', seller_views.seller_discounts, name='seller_discounts'),
]
