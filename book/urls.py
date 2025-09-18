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
    path('basket/', views.basket_view, name='basket_view'),
    path('basket_add/<int:book_id>/', views.basket_add, name='basket_add'),
    path('basket_remove/<int:book_id>/', views.basket_remove, name='basket_remove'),
    path('payment/',views.payment, name='payment' )
]