from django.urls import path
from book import views

urlpatterns = [
    path('', views.home, name='home'),
    path('create/', views.create, name='create'),
    path('<int:book_id>/detail', views.detail, name='detail'),
    path('<int:book_id>/update', views.update, name='update'),
    path('<int:book_id>/delete', views.delete, name='delete'),
]