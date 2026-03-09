from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
import products.views as product_views
from accounts import seller_views
from discounts import views as discount_views

seller_urls = [
    path('dashboard/', seller_views.seller_dashboard),
    path('products/', seller_views.seller_products),
    path('product/add/', seller_views.add_product),
    path('product/edit/<int:pk>/', seller_views.edit_product),
    path('product/delete/<int:pk>/', seller_views.delete_product),
    path('orders/', seller_views.seller_orders),
    path('orders/update/<int:pk>/', seller_views.update_order_status),
    path('discounts/', seller_views.seller_discounts),
    path('discounts/add/', discount_views.add_discount),
    path('discounts/delete/<int:code_id>/', discount_views.delete_discount),
    path('discounts/toggle/<int:code_id>/', discount_views.toggle_discount),
]

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('products/', include('products.urls')),
    path('orders/', include('orders.urls')),
    path('seller/', include((seller_urls, 'seller'))),
    path('discount/', include('discounts.urls')),
    path('superadmin/', include('dashboard.urls')),
    path('chatbot/', include('chatbot.urls')),
    path('', product_views.home, name='home'),
]

# Media files — development aur production dono mein
# (Production mein Railway/Render pe media folder persist nahi hota,
#  lekin uploaded images ke liye zaroor chahiye)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Static files — sirf debug mode mein (production mein whitenoise handle karta hai)
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
