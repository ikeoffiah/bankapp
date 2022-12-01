from django.db import models
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager


class CustomAccountManager(BaseUserManager):


    def create_superuser(self, email, first_name,last_name, password, **other_fields):
        other_fields.setdefault('is_staff',True)
        other_fields.setdefault('is_superuser',True)
        other_fields.setdefault('is_active',True)

        if other_fields.get('is_staff') is not True:
            raise ValueError('Super User must be Staff')

        if other_fields.get('is_superuser') is not True:
            raise ValueError('Super User must be true')

        if other_fields.get('is_active') is not True:
            raise ValueError('Super User must be active')

        return self.create_user(email, first_name,last_name, password, **other_fields)




    def create_user(self, email, first_name,last_name, password, **other_fields):
        if not email:
            raise ValueError('You have to set your email')

        if not first_name:
            raise ValueError('You have to set your first name')

        if not last_name:
            raise ValueError('You have to set your last name')

        email = self.normalize_email(email)
        user = self.model(email=email, first_name= first_name, last_name=last_name, **other_fields)
        user.set_password(password)
        user.save()
        return user







class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=200, default='')
    last_name = models.CharField(max_length=200, default='')
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)

    objects = CustomAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return self.email

    def tokens(self):
        refresh_token = RefreshToken.for_user(self)
        return {
            'refresh':str(refresh_token),
            'access':str(refresh_token.access_token)
        }
