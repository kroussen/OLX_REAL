from django.urls import path


from . import views
from django.contrib.auth import views as auth_views 
from posts.views import favorite_products


urlpatterns = [
    path('login/', views.user_login, name='login'),
    path('profile/', views.profile, name='profile'),
    path('register/', views.register, name='register'),
    path('loginn/', auth_views.LogoutView.as_view(), name='logout'),
    path('favorite_products/', favorite_products, name='favorite_products'),
    path('profile_settings/', views.profile_settings, name='profile_settings'),
    # path('change_password/', views.change_password, name='change_password'),
]
