from posts.models import Cart, CartItem

def cart_items_count_processor(request):
    cart_items_count = 0
    if request.user.is_authenticated:
        cart, _ = Cart.objects.get_or_create(user=request.user)
        cart_items_count = CartItem.objects.filter(cart=cart).count()
    return {'cart_items_count': cart_items_count}