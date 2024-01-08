from django import forms
from users.models import  MyUser
from django.contrib.auth.forms import AuthenticationForm


class LoginForm(AuthenticationForm):
    class Meta:
        model = MyUser
        fields = ['username', 'password']