from django.core.exceptions import ValidationError
from django.db import models
from django.db.models.query import QuerySet
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.contrib.auth.models import Group, Permission


class MyUserManager(BaseUserManager):
    """ClientManager."""

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email address is required')

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)  # Сохранение пользователя
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        user = self.create_user(email, password=password, **extra_fields)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)  # Сохранение суперпользователя

        # Добавление суперпользователю группы и прав
        group = Group.objects.get(name='Superuser')
        user.groups.add(group)
        user.user_permissions.set(Permission.objects.all())

        return user


class MyUser(AbstractBaseUser, PermissionsMixin):

    username = models.CharField(
        verbose_name='Имя',
        max_length=50
    )
    email = models.EmailField(
        verbose_name='почта',
        unique=True,
        max_length=200
    )
    is_staff = models.BooleanField(
        default=False
    )


    user_image = models.URLField(blank=True, null=True, default='https://ростр.рф/assets/img/no-profile.png')
    
    objects = MyUserManager()

    groups = models.ManyToManyField(
        Group,
        verbose_name='groups',
        blank=True,
        related_name='myuser_set',
        related_query_name='user',
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name='user permissions',
        blank=True,
        related_name='myuser_set',
        related_query_name='user',
    )

    REQUIRED_FIELDS = []
    USERNAME_FIELD = 'email'
