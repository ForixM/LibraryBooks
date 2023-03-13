from django.urls import path
from . import views

app_name = 'book'
urlpatterns = [
    # The view for the main page where all books will be displayed
    path('', views.LibraryBook.as_view(), name='index'),

    # The view for creating a book
    path('create/', views.CreateBookView.as_view(), name='create'),

    # The view that will edit an already existing book
    path('edit/<int:num>', views.EditBookView.as_view(), name='edit'),

    # The view that will confirm the deletion of a book
    path('delete/<pk>/', views.DeleteConfirmView.as_view(), name='delete'),

    # The view to display books ready to be bought
    path('shop/', views.ShopView.as_view(), name='shop'),

    # Book purchase confirmation will be displayed in this view.
    path('shop/<int:num>', views.BuyBookView.as_view(), name='buyBook'),

    # User-created books will be displayed in this view.
    path('owned/', views.OwnedBooksView.as_view(), name='ownedBooks'),

    # User-purchased books will be displayed in this view.
    path('purchased/', views.PurchasedBooksView.as_view(), name='purchasedBooks'),
]
