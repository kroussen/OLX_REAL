from django.contrib import admin
from posts.models import Product, City, Country, Cart, CartItem, Favorite

admin.site.register(Product)
admin.site.register(City)
admin.site.register(Country)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Favorite)
