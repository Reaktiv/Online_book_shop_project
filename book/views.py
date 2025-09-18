from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.http import HttpResponse, HttpResponseBadRequest
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
        return HttpResponse("Has no permission!")

    if not request.user.has_perm('book.view_book'):
        return HttpResponse("You have no permission to see!")

    books = Book.objects.filter(published=True)
    search_book = request.POST.get('search_published_book')

    if search_book:
        books = Book.objects.filter(
            Q(title__icontains=search_book) |
            Q(description__icontains=search_book),
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
    books = Book.objects.filter(added_by=request.user, published=False)

    search_book = request.POST.get('search_unpublished_book')

    if search_book:
        books = Book.objects.filter(
            Q(title__icontains=search_book) |
            Q(description__icontains=search_book),
            published=False, added_by=request.user)
    context = {
        'books': books
    }
    return render(request, 'book/unpublished_books.html', context=context)


def my_books(request):
    books = Book.objects.filter(added_by=request.user, published=True)

    search_book = request.POST.get('search_my_published_book')

    if search_book:
        books = Book.objects.filter(
            Q(title__icontains=search_book) |
            Q(description__icontains=search_book),
            published=True, added_by=request.user)
    context = {
        'books': books
    }
    return render(request, 'book/my_books.html', context=context)


def create(request):
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            book = form.save(commit=False)
            book.added_by = request.user
            book.save()
            messages.success(request, f"{book.title} created successfully")
            return redirect('home')
    else:
        form = BookForm()
    context = {
        'form': form
    }
    return render(request, 'book/create.html', context=context)


def detail(request, book_id):
    books = get_object_or_404(Book, id=book_id)
    context = {
        'books': books,

    }
    return render(request, 'book/detail.html', context=context)


def update(request, book_id):
    book = get_object_or_404(Book, id=book_id, added_by=request.user)
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES, instance=book)
        if form.is_valid():
            b_k = form.save()
            messages.success(request, f"Informations of {b_k.title} changed successfully")
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
    messages.warning(request, f"{book.title} changed successfully!")
    return redirect('home')


def basket_view(request):
    # Savatdagi ma'lumotlarni olish, agar bo'sh bo'lsa, bo'sh dict
    basket = request.session.get('basket', {})

    # Faqat savatda mavjud kitoblar ID larini olish
    book_ids = [key for key in basket.keys() if key.isdigit()]
    books = Book.objects.filter(id__in=book_ids).select_related()  # Optimallashtirish uchun select_related

    basket_items = []
    total_price = 0  # Umumiy narxni hisoblash uchun

    for book in books:
        quantity = int(basket[str(book.id)])  # Sonni int ga aylantirish
        basket_items.append({
            'book': book,
            'quantity': quantity,
            'total': book.price * quantity  # Har bir kitobning umumiy narxini qo'shish
        })
        total_price += book.price * quantity

    context = {
        'basket_items': basket_items,
        'total_price': total_price
    }
    return render(request, 'book/basket_view.html', context)


def basket_add(request, book_id):
    if request.method == 'POST':
        try:
            Book.objects.get(id=book_id)
            basket = request.session.get('basket', {})
            basket[str(book_id)] = basket.get(str(book_id), 0) + 1
            request.session['basket'] = basket
            request.session.modified = True
        except Book.DoesNotExist:
            pass
        return redirect('basket_view')
    return HttpResponseBadRequest("Invalid request method")


def basket_remove(request, book_id):
    basket = request.session.get('basket', {})
    book_id_str = str(book_id)

    if book_id_str in basket:
        quantity = int(basket[book_id_str])
        if quantity > 1:
            basket[book_id_str] = quantity - 1  # Miqdorni 1 taga kamaytir
        else:
            del basket[book_id_str]  # Agar 1 bo‘lsa va kamaytirilsa, o‘chirib yubor

        request.session['basket'] = basket
        request.session.modified = True  # Sessiyani yangilash

    return redirect('basket_view')

def payment(request):
    return render(request, 'book/payment.html')
