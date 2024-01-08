from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib import messages
from django.urls import reverse
from django.http import Http404
from django.http import HttpResponse
from django.http import HttpResponseRedirect

from posts.models import Product, City, Cart, CartItem, Favorite
from posts.forms.create_product_form import ProductForm
import stripe


@login_required
def create_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.seller = request.user

            city_name = request.POST.get('city_id')
            city = City.objects.get(name=city_name)
            product.city = city

            # Сохраняем URL изображения вместе с товаром
            image_url = request.session.get('image_url')
            product.image = image_url

            product.save()
            print(f"Product saved: {product.title}")
            return redirect('main_page')  # Перенаправляем на страницу со списком продуктов

    else:
        form = ProductForm()

    return render(request, 'create_product.html', {'form': form})


def get_image(request):
    if request.method == "POST":
        request.session['image_url'] = request.POST.get('image_url')

    return HttpResponse(status=200)


def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)

    is_favorited = False
    if request.user.is_authenticated:
        # Проверяем, добавлен ли товар в избранное для текущего пользователя
        is_favorited = Favorite.objects.filter(user=request.user, advertisement=product).exists()

    is_product_creator = product.seller == request.user

    return render(request, 'product_detail.html', {
        'product': product,
        'is_favorited': is_favorited,
        'is_product_creator': is_product_creator
    })


@login_required
def product_edit(request, pk):
    product = get_object_or_404(Product, pk=pk)

    # Проверяем, является ли текущий пользователь создателем продукта
    if product.seller != request.user:
        raise Http404("У вас нет разрешения на редактирование этого продукта")

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.seller = request.user

            city_name = request.POST.get('city_id')
            city = City.objects.get(name=city_name)
            product.city = city

            # Сохраняем URL изображения вместе с товаром
            image_url = request.session.get('image_url')
            product.image = image_url

            product.save()
            return redirect('posts:product_detail', pk=pk)  # Перенаправляем на страницу с деталями продукта
    else:
        form = ProductForm(instance=product)

    return render(request, 'edit_product.html', {'form': form})


def get_cities(request):
    query = request.GET.get('query', '').capitalize()  # Получаем запрос пользователя и делаем первую букву заглавной
    cities = list(City.objects.filter(name__istartswith=query).values_list('name', flat=True))
    return JsonResponse({'cities': cities})


@login_required
def add_to_cart(request, product_id):
    product = Product.objects.get(pk=product_id)
    cart, _ = Cart.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)

    return redirect('posts:product_detail', pk=product_id)


@login_required
def remove_from_cart(request, product_id):
    if request.method == 'POST':
        product = Product.objects.get(pk=product_id)
        cart = Cart.objects.get(user=request.user)
        cart_item = CartItem.objects.get(cart=cart, product=product)
        cart_item.delete()
        return redirect('posts:buy_product')

    return HttpResponseRedirect('/')


@login_required
def buy_now(request, product_id):
    product = Product.objects.get(pk=product_id)
    cart, _ = Cart.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)

        # Перенаправление на страницу с корзиной
        return redirect('posts:buy_product')

    return redirect('product_detail', product_id=product_id)


@login_required
def buy_product(request):
    # Получение корзины пользователя, если она есть
    cart, _ = Cart.objects.get_or_create(user=request.user)
    cart_items = CartItem.objects.filter(cart=cart)

    total_quantity = sum(item.quantity for item in cart_items)
    total_price = sum(item.total_price() for item in cart_items)

    return render(request, 'buy_product.html', {
        'cart_items': cart_items,
        'total_quantity': total_quantity,
        'total_price': total_price,
    })


@login_required
def cart_items_count(request):
    cart_items_count = 0
    if request.user.is_authenticated:
        cart, _ = Cart.objects.get_or_create(user=request.user)
        cart_items_count = CartItem.objects.filter(cart=cart).count()
    return JsonResponse({'cart_items_count': cart_items_count})


@login_required
def add_to_favorites(request, product_id):
    product = get_object_or_404(Product, pk=product_id)

    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'add':
            Favorite.objects.get_or_create(user=request.user, advertisement=product)
        elif action == 'remove':
            Favorite.objects.filter(user=request.user, advertisement=product).delete()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def favorite_products(request):
    user_favorites = Favorite.objects.filter(user=request.user)
    return render(request, 'favorite_products.html', {'user_favorites': user_favorites})


stripe.api_key = "sk_test_51OOfJrDFP7obIEXtlQ1Y32rjDj8EVzrtNe1Ppx1Cc3c63EKeLyDyClNdGKIoKNUnDUV2Y1aTvH9k8a2KCuGjj54H00nT6zm8XM"


def create_checkout_session(request):
    # Получение корзины пользователя, если она есть
    cart, _ = Cart.objects.get_or_create(user=request.user)
    cart_items = CartItem.objects.filter(cart=cart)

    line_items = []  # Список товаров для сеанса оплаты
    total_price = 0

    for cart_item in cart_items:
        product = cart_item.product
        line_items.append({
            'price_data': {
                'currency': 'usd',
                'unit_amount': int(product.price * 100),  # Умножаем цену на 100 (в центах для Stripe)
                'product_data': {
                    'name': product.title,  # Название продукта
                },
            },
            'quantity': cart_item.quantity,
        })

        total_price += product.price * cart_item.quantity * 100  # Общая цена всех товаров в корзине

    try:
        success_url = request.build_absolute_uri(reverse('posts:success_url'))
        cancel_url = request.build_absolute_uri(reverse('posts:cancel_url'))
        # Создание сеанса оплаты через Stripe
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=line_items,
            mode='payment',
            success_url=success_url,  # URL для перенаправления после успешной оплаты
            cancel_url=cancel_url,  # URL для перенаправления после отмены оплаты
        )

        return checkout_session.url  # Возвращает URL для оплаты

    except stripe.error.StripeError as e:
        # Обработка ошибок Stripe
        return str(e)  # Возвращает сообщение об ошибке


def checkout(request):
    if request.method == 'POST':
        session_id = create_checkout_session(request)
        return redirect(session_id)  # Перенаправление на страницу оплаты
    return render(request, 'checkout.html')


def success_url(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = CartItem.objects.filter(cart=cart)

    if created:
        return redirect('posts:buy_product')

    # Удаляем товары из корзины после успешной оплаты
    cart_items.delete()
    
    messages.success(request, 'Оплата прошла успешно', extra_tags='alert-success')
    return redirect('posts:buy_product')


def cancel_url(request):
    # Код для обработки отмены оплаты
    messages.success(request, 'Оплата отменена', extra_tags='alert-danger')
    return redirect('posts:buy_product')


# def search_products(request):
#     search_query = request.GET.get('search', None)
#     categories = Category.objects.all()

#     if search_query:
#         products = Product.objects.filter(Q(title__icontains=search_query) | Q(description__icontains=search_query))
#     else:
#         products = Product.objects.all()

#     context = {
#         'products': products,
#         'categories': categories,
#         'search_query': search_query,
#     }
#     return render(request, 'product_list.html', context)
