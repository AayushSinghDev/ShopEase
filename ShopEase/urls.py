from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
import products.views as product_views
from accounts import seller_views, admin_views
from discounts import views as discount_views

# ── Seller URLs ───────────────────────────────────────────────
seller_urls = [
    path('dashboard/',                      seller_views.seller_dashboard),
    path('products/',                       seller_views.seller_products),
    path('product/add/',                    seller_views.add_product),
    path('product/edit/<int:pk>/',          seller_views.edit_product),
    path('product/delete/<int:pk>/',        seller_views.delete_product),
    path('orders/',                         seller_views.seller_orders),
    path('orders/update/<int:pk>/',         seller_views.update_order_status),
    path('discounts/',                      seller_views.seller_discounts),
    path('discounts/add/',                  discount_views.add_discount),
    path('discounts/delete/<int:code_id>/', discount_views.delete_discount),
    path('discounts/toggle/<int:code_id>/', discount_views.toggle_discount),
]

# ── Admin Panel URLs ──────────────────────────────────────────
admin_panel_urls = [
    path('sellers/',   admin_views.admin_sellers,   name='admin_sellers'),
    path('customers/', admin_views.admin_customers, name='admin_customers'),
    path('products/',  admin_views.admin_products,  name='admin_products'),
    path('orders/',    admin_views.admin_orders,    name='admin_orders'),
]

# ── Main URLs ─────────────────────────────────────────────────
urlpatterns = [
    path('admin/',       admin.site.urls),
    path('accounts/',    include('accounts.urls')),
    path('products/',    include('products.urls')),
    path('cart/',        include('orders.urls')),
    path('seller/',      include((seller_urls, 'seller'))),
    path('discount/',    include('discounts.urls')),
    path('admin-panel/', include((admin_panel_urls, 'admin_panel'))),
    path('',             product_views.home, name='home'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,  document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)