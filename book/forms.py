from django.forms import ModelForm

from django import forms
from book.models import Book


class BookForm(ModelForm):

    class Meta:
        model = Book
        fields = ('added_by',   'title', 'author', 'description',  'photo', 'published')

