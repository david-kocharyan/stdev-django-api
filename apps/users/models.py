import os
import time

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from apps.core.models import TimeStampedAbstractModel


def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT / uploads/ users/
    upload_to = 'uploads/users/'
    ext = filename.split('.')[-1]
    if instance:
        filename = 'user_{}.{}'.format(instance.first_name, instance.last_name, ext)
    else:
        filename = 'user_{}.{}'.format(int(time.time()), ext)

    return os.path.join(upload_to, filename)


class UserManager(BaseUserManager):

    def create_user(self, email, password=None):
        if not email or not password:
            raise ValueError('User must have an email address and password')
        email = email.lower()
        user = self.model(email=self.normalize_email(email))
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password):
        email = email.lower()
        user = self.create_user(email, password=password)
        user.is_staff, user.is_superuser, user.is_active = True, True, True
        user.role, user.status = None, None
        user.save()
        return user


class User(AbstractBaseUser, PermissionsMixin, TimeStampedAbstractModel):
    email = models.EmailField(verbose_name='Email Address', unique=True)
    password = models.CharField(verbose_name='Password', max_length=128)
    first_name = models.CharField(verbose_name='First Name', max_length=150)
    last_name = models.CharField(verbose_name='Last Name', max_length=150)
    image = models.ImageField(verbose_name="Image", upload_to=user_directory_path)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = UserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    @property
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return self.email
