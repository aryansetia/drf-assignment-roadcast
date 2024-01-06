from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from .managers import CustomUserManager


class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(_("email address"), unique=True)
    name = models.CharField(_("name"), max_length=255)  # Add the 'name' field

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['name']  # Add 'name' to the required fields

    objects = CustomUserManager()

    def __str__(self):
        return self.email


class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='profile')
    friends = models.ManyToManyField(CustomUser, related_name='friends', blank=True)
    friend_requests_sent = models.ManyToManyField(CustomUser, related_name='friend_requests_sent', blank=True)
    friend_requests_received = models.ManyToManyField(CustomUser, related_name='friend_requests_received', blank=True)

    def __str__(self): 
        return self.user.email