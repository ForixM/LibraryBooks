from django.contrib import admin
from django.urls import path
from . import views

app_name = 'book'
urlpatterns = [
    path('', views.LibraryBook.as_view(), name='index'),
    path('<int:num>/', views.book, name='book'),
    path('create/', views.createBook, name='create'),
    path('edit/<int:num>', views.editBook, name='edit'),
    path('delete/<int:num>', views.confirmDelete, name='delete'),
]
