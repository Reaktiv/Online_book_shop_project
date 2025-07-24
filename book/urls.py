from django.urls import path
from book import views

urlpatterns = [
    path('', views.home, name='home'),
    path('create/', views.create, name='create'),
    path('<int:blog_id>/detail', views.detail, name='detail'),
    path('<int:blog_id>/update', views.update, name='update'),
    path('<int:blog_id>/delete', views.delete, name='delete'),
]