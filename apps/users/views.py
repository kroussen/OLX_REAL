from django.shortcuts import render , redirect
from django.contrib.auth.forms import AuthenticationForm
from .forms.registration_form import RegistrationForm
from .forms.editing_user_data_form import EditingUserDataForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse
from .forms.custom_password_change_form import CustomPasswordChangeForm
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash

from posts.models import Product, Favorite


@login_required
def profile(request):
    if not request.user.is_authenticated:
        messages.error(request, 'Вы не авторизованы, войдите в систему, чтобы продолжить')
        return redirect(reverse('login'))  # Перенаправление на страницу Авторизации
    
    user_advertisements = Product.objects.filter(seller=request.user)
    favorites = Favorite.objects.filter(user=request.user)

    # Если пользователь аутентифицирован, код ниже будет выполнен
    user_account = request.user 
    return render(request, 'profile.html', {'user_account': user_account, 'user_advertisements': user_advertisements, 'favorites': favorites})


@login_required
def profile_settings(request):
    user = request.user
    if request.method == 'POST':
        if 'change_password' in request.POST:
            # Если пользователь пытается изменить пароль
            form = CustomPasswordChangeForm(user=request.user, data=request.POST)
            if form.is_valid():
                user = form.save()
                update_session_auth_hash(request, user)
                messages.success(request, 'Пароль успешно изменен!')
                return redirect('profile')
            else:
                messages.error(request, 'Пожалуйста, исправьте ошибки в форме смены пароля.')
        else:
            # Если пользователь пытается изменить имя, email или аватар
            form = EditingUserDataForm(request.POST, request.FILES, instance=user)
            if form.is_valid():
                form.save()
                messages.success(request, 'Информация успешно обновлена!')
                return redirect('profile')
            else:
                messages.error(request, 'Форма содержит ошибки')
    else:
        form = EditingUserDataForm(instance=user)
    return render(request, 'profile_settings.html', {'form': form})


# @login_required
# def profile_settings(request):
#     user = request.user

#     if request.method == 'POST':
#         form = EditingUserDataForm(request.POST, request.FILES, instance=user)
#         if form.is_valid():
#             form.save()
#             messages.success(request, 'Информация успешно обновлена!')
#             return redirect('profile')
#         else:
#             messages.error(request, 'Форма содержит ошибки')

#     else:
#         form = EditingUserDataForm(instance=user)

#     return render(request, 'profile_settings.html', {'form': form})


# @login_required
# def change_password(request):
#     if request.method == 'POST':
#         form = CustomPasswordChangeForm(user=request.user, data=request.POST)
#         if form.is_valid():
#             user = form.save()  # Сохранение нового пароля пользователя в базе данных
#             update_session_auth_hash(request, user)  # Обновление сессии пользователя после смены пароля
#             messages.success(request, 'Пароль успешно изменен!')
#             return redirect('profile')  # Перенаправление на страницу профиля
#         else:
#             messages.error(request, 'Пожалуйста, исправьте ошибки в форме смены пароля.')
#     else:
#         form = CustomPasswordChangeForm(request.user)
#     return render(request, 'change_password.html', {'form': form})


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            # Сохранение формы, если она валидна
            user = form.save(commit=False)  # Создание пользователя, но не сохранение в базе данных пока
            user.set_password(form.cleaned_data['password1'])  # Установка пароля пользователя
            user.save()  # Сохранение пользователя в базе данных

            login(request, user)  # Вход пользователя после успешной регистрации
            return redirect('profile')  # Перенаправление на страницу профиля после регистрации

    else:
        form = RegistrationForm()  # Создание новой формы для регистрации

    return render(request, 'register.html', {'form': form})  # Отображение формы на странице регистрации


def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            email = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('profile') 
    else:
        form = AuthenticationForm()
        if request.GET.get('next', None):
            messages.warning(request, 'Вы не авторизованы, войдите в систему, чтобы продолжить')
    return render(request, 'login.html', {'form': form})
