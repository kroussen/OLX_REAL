from django import forms
from users.models import  MyUser


class EditingUserDataForm(forms.ModelForm):
    user_image = forms.CharField(widget=forms.HiddenInput())

    class Meta:
        model = MyUser
        fields = ['username', 'email', 'user_image']

