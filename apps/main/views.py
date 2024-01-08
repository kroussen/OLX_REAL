from django.template.loader import get_template
from django.http import HttpResponse
from django.shortcuts import render

from posts.models import Product


def main_page(request):
    products = Product.objects.all()  # Получение всех товаров из базы данных
    return render(request, 'main.html', {'products': products})
