from django.db import models
from users.models import MyUser


class Country(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class City(models.Model):
    name = models.CharField(max_length=100)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Product(models.Model):
    title = models.CharField(max_length=255, verbose_name='Название')
    description = models.TextField(max_length=255, verbose_name='Описание')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена')
    date_posted = models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации')
    seller = models.ForeignKey(MyUser, on_delete=models.CASCADE, verbose_name='Продавец')
    image_url = models.URLField(blank=True, null=True, verbose_name='URL изображения')
    image = models.ImageField(upload_to='', blank=True, verbose_name='Фотография')
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Город')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'


class Cart(models.Model):
    user = models.OneToOneField(MyUser, on_delete=models.CASCADE)

    def __str__(self):
        return f"Корзина пользователя {self.user.username}"


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)  # Количество единиц товара в корзине

    def total_price(self):
        return self.product.price * self.quantity

    def __str__(self):
        return f"{self.product.title} в корзине"
    

class Favorite(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    advertisement = models.ForeignKey(Product, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'advertisement')
