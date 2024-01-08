from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from apps.main import views  # Импортируйте модуль views, содержащий представления


urlpatterns = [
    path('admin/', admin.site.urls),
    path('main/', include('users.urls')),
    path('main/', include('posts.urls')),  # Включаем URL-адреса из posts.urls
    path('main/', views.main_page, name='main_page'),
]
urlpatterns += static(
    settings.STATIC_URL,
    document_root=settings.STATIC_ROOT
)
urlpatterns += static(
    settings.MEDIA_URL,
    document_root=settings.MEDIA_ROOT
)
