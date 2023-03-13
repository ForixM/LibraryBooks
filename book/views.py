from django.views import generic
from .models import Book, Wallet
from django.shortcuts import render, HttpResponseRedirect, reverse, get_object_or_404, redirect
from django.urls import reverse_lazy

from .forms import EditBookForm, CreateBookForm, ConfirmationForm


# The main page view. All books that are stored in the database will be returned as a queryset usable in the HTML code.
class LibraryBook(generic.TemplateView):
    template_name = "book/index.html"


# This view will display the books that the connected user have created and sold on the shop.
class OwnedBooksView(generic.ListView):
    # The choice to use the same template as purchased books view was made on purpose because they both have almost
    # the same layout
    template_name = 'book/books.html'
    model = Book
    context_object_name = 'library'

    # This def will give extra context variables in addition to existing context variables to the template
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'BOOK MANAGER'
        context['owned'] = True
        return context

    def get_queryset(self):
        return Book.objects.filter(owner_id=self.request.user.id)

    # This function is called before the rendered page will be sent to the client in order to check if he is logged-in
    # or not.
    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return HttpResponseRedirect(reverse('book:index'))
        return super().dispatch(request, *args, **kwargs)


# This view will display the books purchased by the connected user in the shop.
class PurchasedBooksView(generic.ListView):
    # The choice to use the same template as owned books view was made on purpose because they both have almost
    # the same layout
    template_name = 'book/books.html'
    model = Book
    context_object_name = 'library'

    # This def will give extra context variables in addition to existing context variables to the template
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'PURCHASED BOOKS'
        context['owned'] = False
        return context

    def get_queryset(self):
        return Book.objects.filter(purchasers__id=self.request.user.id)

    # This function is called before the rendered page will be sent to the client in order to check if he is logged-in
    # or not.
    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return HttpResponseRedirect(reverse('book:index'))
        return super().dispatch(request, *args, **kwargs)


# This view have a form to edit book information in the database
class EditBookView(generic.FormView):
    template_name = 'book/edit.html'
    form_class = EditBookForm
    success_url = reverse_lazy('book:ownedBooks')

    # A custom created def in order to retrieve a specific book related to the id given in the url
    def get_book(self):
        try:
            num = self.kwargs['num']
            book = Book.objects.get(pk=num)
            return book
        except(KeyError, Book.DoesNotExist):
            return None

    # This def will give extra context variables in addition to existing context variables to the template
    def get_context_data(self, **kwargs):
        try:
            book = self.get_book()
        except(KeyError, Book.DoesNotExist):
            return HttpResponseRedirect(reverse('book:index'))
        context = super().get_context_data(**kwargs)
        context['book'] = book
        return context

    # This def will be called when the client will submit the form. it will update the book fields only if the 'edit'
    # submit input have been pressed. If the 'cancel' submit input have been pressed, the update book process will be skipped.
    def form_valid(self, form):
        book = self.get_book()
        if 'edit' in self.request.POST:
            form.update_book(book)
        return super().form_valid(form)

    # This function is called before the rendered page will be sent to the client in order to check if he is logged-in
    # or not. It will also check if the book exists and if the connected user is the creator of the book
    def dispatch(self, request, *args, **kwargs):
        book = self.get_book()
        if book is None or (not self.request.user.is_authenticated or book.owner.id != self.request.user.id):
            return HttpResponseRedirect(reverse('book:index'))
        return super().dispatch(request, *args, **kwargs)


# This generic form view will create a book and add it to the database
class CreateBookView(generic.FormView):
    template_name = 'book/create.html'
    form_class = CreateBookForm  # The form that the view will be based. It is located in forms.py
    success_url = reverse_lazy('book:ownedBooks')

    # This function will be called when the user will submit the form
    def form_valid(self, form):
        book = form.create_book(self.request.user)
        return HttpResponseRedirect(reverse('book:ownedBooks'))

    # This function is called before the page will be sent in order to verify if the user is authenticated
    # Otherwise, it will redirect it to the main page.
    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return HttpResponseRedirect(reverse('book:index'))
        return super().dispatch(request, *args, **kwargs)


# This view have the purpose to confirm if the user wants to delete the book or not.
class DeleteConfirmView(generic.DeleteView):
    template_name = 'book/delete.html'
    model = Book
    success_url = reverse_lazy('book:ownedBooks')

    # This def will be called when the user will submit the form. If the client clicked on 'cancel' submit input,
    # he will be directly redirected to the ownedBooks view in order to avoid the book suppression performed in
    # the parent form_valid def.
    def form_valid(self, form):
        if 'cancel' in self.request.POST:
            return HttpResponseRedirect(reverse('book:ownedBooks'))
        return super().form_valid(form)

    # This function is called before the page will be sent in order to verify if the user is authenticated and if
    # the creator of the book matches with the connected user.
    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return HttpResponseRedirect(reverse('book:index'))
        if self.get_object().owner.id is not request.user.id:
            return HttpResponseRedirect(reverse('book:ownedBooks'))
        return super().dispatch(request, *args, **kwargs)


# This view will display the book on sale in the shop. The connected user can buy any book he wants only if he has
# enough money in his wallet.
class ShopView(generic.ListView):
    template_name = 'book/shop.html'
    model = Book
    context_object_name = 'books'

    # This def will give extra context variables in addition to existing context variables to the template
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            context['wallet'] = Wallet.objects.get(owner_id=self.request.user.id)
        except(KeyError, Wallet.DoesNotExist):
            return context
        return context

    # This get_queryset override def do a special data manipulation. It will create a dictionary in order to know
    # for each book if he had already been purchased. Owned book will not be added to the dictionary.
    def get_queryset(self):
        books = Book.objects.all()
        toReturn = {}
        for book in books:
            purchased = False
            for purchaser in book.purchasers.all():
                if purchaser.id is self.request.user.id:
                    purchased = True
            if not book.owner.id == self.request.user.id:
                toReturn[book] = purchased
        return toReturn


# This view is a transaction confirmation in order to make sure that the user wants to buy a book or no.
class BuyBookView(generic.FormView):
    template_name = 'book/buy.html'
    form_class = ConfirmationForm
    success_url = reverse_lazy('book:shop')

    # This def will be called after the user have submitted the form.
    # If the client pressed the 'yes' submit input, verifications will be made in order to see if the connected user
    # have enough money and if the connected user is not the one who sold the book.
    # If all conditions have been satisfied, money will be retrieved from the user that purchased the book to the one
    # who sold the book.
    def form_valid(self, form):
        if 'yes' in self.request.POST:
            book = Book.objects.get(pk=self.kwargs['num'])
            if not book.purchasers.all().contains(self.request.user):
                wallet = Wallet.objects.get(owner_id=self.request.user.id)
                if wallet.balance >= book.price:
                    wallet.balance -= book.price
                    wallet.save()
                    owner_wallet = Wallet.objects.get(owner_id=book.owner.id)
                    owner_wallet.balance += book.price
                    owner_wallet.save()
                    book.purchasers.add(self.request.user)
                    book.save()
        return super().form_valid(form)

    # This def will give extra context variables in addition to existing context variables to the template
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['book'] = Book.objects.get(pk=self.kwargs['num'])
        return context

    # This function is called before the page will be sent in order to verify if the user is authenticated
    # Otherwise, it will redirect it to the shop page.
    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return HttpResponseRedirect(reverse('book:shop'))
        return super().dispatch(request, *args, **kwargs)
