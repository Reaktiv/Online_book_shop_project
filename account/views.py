from django.contrib import messages
from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import render, redirect

from account.forms import CustomUserCreationForm, CustomUserChangeForm, ProfileChangeForm


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, f"{user.username} muvoffaqqiyatli yaratildi!")
            return redirect('login')
    else:
        form = CustomUserCreationForm()

    context = {
        "form": form
    }
    return render(request, 'account/register.html', context=context)


