from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    path('', views.shop, name='shop'),
    path('home/', views.home, name='home'),
    path('detail/<int:pk>/', views.product_detail, name='product_detail'),
    path('categories/', views.category_list, name='category_list'),

    # Wishlist
    path('wishlist/', views.wishlist_view, name='wishlist'),
    path('wishlist/add/<int:product_id>/', views.add_to_wishlist, name='add_to_wishlist'),
    path('wishlist/remove/<int:product_id>/', views.remove_from_wishlist, name='remove_from_wishlist'),

    # Reviews
    path('review/add/<int:product_id>/', views.add_review, name='add_review'),
    path('review/delete/<int:review_id>/', views.delete_review, name='delete_review'),

    # Comparison
    path('compare/', views.compare_view, name='compare'),
    path('compare/add/<int:product_id>/', views.compare_add, name='compare_add'),
    path('compare/remove/<int:product_id>/', views.compare_remove, name='compare_remove'),
    path('compare/clear/', views.compare_clear, name='compare_clear'),
]
