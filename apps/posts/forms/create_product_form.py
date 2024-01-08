from django import forms
from posts.models import Product


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['title', 'description', 'price', 'image_url', 'image']
        widgets = {
            'seller': forms.HiddenInput(attrs={'readonly': 'readonly'}),  # Установите поле "seller" в режим только чтения и скройте его
        }
