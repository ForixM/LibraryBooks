from django import forms
from .models import Book
from django.utils import timezone


# This is an empty form used for confirmation views
class ConfirmationForm(forms.Form):
    pass


# This form will store the fields that will be modified in the book
class EditBookForm(forms.Form):
    title = forms.CharField()
    author = forms.CharField()
    description = forms.CharField()
    gender = forms.CharField()
    num_pages = forms.IntegerField()
    price = forms.FloatField()

    def is_valid(self):
        if float(self.data.get('price')) < 0 or float(self.data.get('num_pages')) < 0:
            return False
        return super().is_valid()

    # This custom def will apply the book update in the database
    def update_book(self, book):
        book.title = self.data['title']
        book.author = self.data['author']
        book.description = self.data['description']
        book.gender = self.data['gender']
        book.num_pages = self.data['num_pages']
        book.price = self.data['price']
        book.save()


# This class-based form will store the fields in order to create a new book
class CreateBookForm(forms.Form):
    title = forms.CharField()
    author = forms.CharField()
    description = forms.CharField()
    gender = forms.CharField()
    num_pages = forms.IntegerField()
    price = forms.FloatField()

    def is_valid(self):
        if float(self.data.get('price')) < 0 or float(self.data.get('num_pages')) < 0:
            return False
        return super().is_valid()

    # This custom def will apply the book create in the database
    def create_book(self, user):
        now = timezone.now()
        book = Book(title=self.data['title'], author=self.data['author'], description=self.data['description'],
                    gender=self.data['gender'], num_pages=self.data['num_pages'], publication_date=now, owner=user,
                    price=self.data['price'])
        book.save()
        return book
