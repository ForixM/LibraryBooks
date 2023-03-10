from django.urls import path
from . import views

app_name = 'book'
urlpatterns = [
    path('', views.LibraryBook.as_view(), name='index'), #The view for the main page where all books will be displayed
    path('<int:bookId>/', views.ViewBook.as_view(), name='book'), #The view where a specific book informations will be displayed
    path('create/', views.CreateBookView.as_view(), name='create'), #The view for creating a book
    path('edit/<int:num>', views.EditBookView.as_view(), name='edit'), #The view that will edit an already existing book
    path('delete/<int:num>', views.confirmDelete, name='delete') #The 'ghost' view that will delete a book
]
