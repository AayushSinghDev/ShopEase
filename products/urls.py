# from django.urls import path
# from . import views

# app_name = 'products'

# urlpatterns = [
#     path('', views.product_list, name='product_list'),
#     path('<int:pk>/', views.product_detail, name='product_detail'),
#     path('add/', views.add_product, name='add_product'),
#     path('category/', views.category_list, name='category_list'),
# ]


from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    path('', views.shop, name='shop'),
    path('detail/<int:pk>/', views.product_detail, name='product_detail'),
    path('category/', views.category_list, name='category_list'),
]