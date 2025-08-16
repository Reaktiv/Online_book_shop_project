
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from book.models import Book
from book.forms import BookForm
from django.contrib.auth.models import Permission
from django.contrib import messages

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

def unpublished_books(request):
    if request.user.is_superuser:
        book = Book.objects.filter(published=False)
    else:
        book = Book.objects.filter(added_by=request.user ,published=False)
    context = {
        'books': book
    }
    return render(request, 'book/unpublished_books.html', context=context)

def my_books(request):
    book = Book.objects.filter(added_by=request.user, published=True)
    context = {
        'books': book
    }
    return render(request, 'book/my_books.html', context=context)


def create(request):
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            book = form.save(commit=False)
            book.added_by = request.user
            book.save()
            messages.success(request, f"{book.title} kitobi muvaffaqiyatli yaratildi!")
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
    book = get_object_or_404(Book, id=book_id, added_by=request.user)
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES, instance=book)
        if form.is_valid():
            b_k = form.save()
            messages.success(request, f"{b_k.title} ning malumotlari muvaffaqiyatli o'zgartirildi!")
            return redirect('home')
    else:
        form = BookForm(instance=book)
    context = {
        'form': form,
        'book': book,
    }
    return render(request, 'book/update.html', context=context)


def delete(request, book_id):
    book = get_object_or_404(Book, id=book_id, added_by=request.user)
    book.delete()
    messages.warning(request, f"{book.title} kitobi muvaffaqiyatli o'chirildi!")
    return redirect('home')



