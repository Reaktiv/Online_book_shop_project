from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include, reverse_lazy
from django.views.generic import TemplateView

from account import views as account_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('book.urls')),
    path('account/', include('account.urls')),
    path('test-email/', account_views.test_send_email, name = 'test_email'),
    path('email-sent/', TemplateView.as_view(
        template_name='mail/send_mail_success.html'
    ), name = 'send_mail_success'),

]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
