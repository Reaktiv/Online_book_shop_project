from django.urls import path
from book import views

urlpatterns = [
    path('', views.home, name='home'),
    path('create/', views.create, name='create'),
    path('<int:book_id>/detail', views.detail, name='detail'),
    path('<int:book_id>/update', views.update, name='update'),
    path('<int:book_id>/delete', views.delete, name='delete'),
    path('/my_books', views.my_books, name='my_books'),
    path('/unpublished_books', views.unpublished_books, name='unpublished_books'),
]