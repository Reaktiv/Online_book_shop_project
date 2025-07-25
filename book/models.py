from django.db import models
from django.forms import ModelForm
from django.conf import settings
from account.models import CustomUser


class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    added_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True, related_name='books')
    description = models.TextField(max_length=500)
    photo = models.ImageField(upload_to='book_photos/')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    published = models.BooleanField(default=True)

    def __str__(self):
        return self.title



