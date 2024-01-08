from django.urls import path
from . import views

from posts.views import product_detail


urlpatterns = [
    path('', views.main_page, name='main'),  # Указываем представление для главной страницы
    # path('create/', views.create_product, name='create_product'),
    # path('product/<int:pk>/', product_detail, name='product_detail'),
]
