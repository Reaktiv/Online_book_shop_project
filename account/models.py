from django.db import models
from django.contrib.auth.models import AbstractUser

from config.settings import AUTH_USER_MODEL


class CustomUser(AbstractUser):
    phone = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(unique=True)
    USERNAME_FIELD = 'email'  # login
    REQUIRED_FIELDS = ['username', 'phone']

    def __str__(self):
        return self.username

    class Meta:
        db_table = 'auth_user'

