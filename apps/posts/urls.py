from django.urls import path
from . import views

app_name = 'posts'  # Добавьте пространство имен для приложения posts

urlpatterns = [
    path('create/', views.create_product, name='create_product'),
    path('product/<int:pk>/', views.product_detail, name='product_detail'),
    path('product/edit/<int:pk>/', views.product_edit, name='product_edit'),
    path('get_cities/', views.get_cities, name='get_cities'),
    path('add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove_from_cart/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('buy_now/<int:product_id>/', views.buy_now, name='buy_now'),   
    path('buy_product/', views.buy_product, name='buy_product'),
    path('cart_items_count/', views.cart_items_count, name='cart_items_count'),
    path('checkout/', views.checkout, name='checkout'),
    path('get_image/', views.get_image, name='get_image'),
    path('add_to_favorites/<int:product_id>/', views.add_to_favorites, name='add_to_favorites'),
    path('success/', views.success_url, name='success_url'),
    path('cancel_url/', views.cancel_url, name='cancel_url'),
]
