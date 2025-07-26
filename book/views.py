from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from book.models import Book
from book.forms import BookForm
from django.contrib.auth.models import Permission


@login_required
def home(request):
    try:
        perm = Permission.objects.get(codename='view_book')
        request.user.user_permissions.add(perm)
    except Permission.DoesNotExist:
        return HttpResponse("Ruxsat mavjud emas!")

    if not request.user.has_perm('book.view_book'):
        return HttpResponse("Sizni ko‘rishga huquqingiz yo‘q!")

    books = Book.objects.filter(published=True)
    search_book = request.GET.get('search_blog')

    if search_book:
        books = Book.objects.filter(
            Q(title__icontains=search_book) |
            Q(content__icontains=search_book),
            published=True)

    type_choices = dict(Book._meta.get_field('type').choices) if hasattr(Book, 'type') else {}
    keys = type_choices.keys()
    values = type_choices.values()


    context = {
        "filter_keys": keys,
        "filter_values": values,
        "books": books,
    }

    return render(request, 'book/home.html', context=context)





def create(request):
    if not request.user.has_perm('book.add_book'):
        return HttpResponse('Sizni blog qo`shishga huquqingiz yo`q!')
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            book = form.save(commit=False)
            book.author = request.user
            book.save()

            return redirect('home')
    else:
        form = BookForm()
    context = {
        'form': form
    }
    return render(request, 'book/create.html', context=context)


def detail(request, book_id):
    book = get_object_or_404(Book, id=book_id)

    context = {
        'book': book,

    }
    return render(request, 'book/detail.html', context=context)




def update(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES, instance=book)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = BookForm(instance=book)
    context = {
        'form': form,
        'book': book,
        'book_id': book_id
    }
    return render(request, 'book/update.html', context=context)


def delete(request, book_id):
    book = get_object_or_404(Book, id=book_id, author=request.user)
    book.delete()
    return redirect('home')


