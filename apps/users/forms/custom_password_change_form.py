from django import forms
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import authenticate

class CustomPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(
        label='Введите старый пароль',
        widget=forms.PasswordInput(attrs={'class': 'form-control mb-3'}),
    )

    new_password1 = forms.CharField(
        label='Введите новый пароль',
        widget=forms.PasswordInput(attrs={'class': 'form-control mb-3'}),
    )

    new_password2 = forms.CharField(
        label='Повторите новый пароль',
        widget=forms.PasswordInput(attrs={'class': 'form-control mb-3'}),
    )

    def clean_old_password(self):
        old_password = self.cleaned_data.get('old_password')
        user = self.user

        # Проверка текущего пароля пользователя
        if not authenticate(username=user.username, password=old_password):
            raise forms.ValidationError('Неверный текущий пароль')

        return old_password

    def clean(self):
        cleaned_data = super().clean()
        new_password1 = cleaned_data.get('new_password1')
        new_password2 = cleaned_data.get('new_password2')

        # Проверка на совпадение новых паролей
        if new_password1 != new_password2:
            raise forms.ValidationError('Новые пароли не совпадают')

        return cleaned_data