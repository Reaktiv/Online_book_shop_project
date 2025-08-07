from django.db import models
from account.models import CustomUser
from config.settings import AUTH_USER_MODEL


class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    added_by = models.ForeignKey(AUTH_USER_MODEL,on_delete=models.CASCADE, related_name='books', default=2)
    description = models.TextField(max_length=500)
    photo = models.ImageField(upload_to='book_photos/')
    created_at = models.DateTimeField(auto_now_add=True)
    published = models.BooleanField(default=True)

    def __str__(self):
        return self.title



