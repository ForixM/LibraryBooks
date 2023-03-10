from django.views import generic
from .models import Book
from django.shortcuts import render, HttpResponseRedirect, reverse, get_object_or_404, redirect

from .forms import EditBookForm, CreateBookForm, SearchBookForm


# The main page view. All books that are stored in the database will be returned as a queryset usable in the HTML code.
class LibraryBook(generic.FormView):
    template_name = "book/index.html"
    form_class = SearchBookForm
    success_url = '/'

    def get_context_data(self, **kwargs):
        if self.request.user.is_authenticated:
            return {
                'library': Book.objects.filter(user_id_id=self.request.user.id)
            }
        else:
            return None

    def form_valid(self, form):
        print('valid: ', form.search_books())
        return super().form_valid(form)

    # def get_queryset(self):
    #     if self.request.user.is_authenticated:
    #         return Book.objects.filter(user_id_id=self.request.user.id)
    #     else:
    #         return None

# This view will retrieve the book id from the url, and tries to find it in the database.
# If the book exists in the database, the view with the book informations will be displayed.
# Otherwise, the page will be automatically redirected to the main page (LibraryBook view).
class ViewBook(generic.ListView):
    template_name = "book/book.html"
    context_object_name = "book"

    def get_queryset(self):
        self.book = get_object_or_404(Book, pk=self.kwargs['bookId'])
        return self.book

    def dispatch(self, request, *args, **kwargs):
        try:
            book = Book.objects.get(pk=self.kwargs['bookId'])
        except(KeyError, Book.DoesNotExist):
            return redirect('/books/')
        if self.request.user.id != book.user_id.id:
            return redirect('/books/')
        return super().dispatch(request, *args, **kwargs)

# This view have a form to edit book informations in the database
class EditBookView(generic.FormView):
    template_name = 'book/edit.html'
    form_class = EditBookForm

    def get_book(self):
        try:
            num = self.kwargs['num']
            book = Book.objects.get(pk=num)
            return book
        except(KeyError, Book.DoesNotExist):
            return None

    def get_context_data(self, **kwargs):
        try:
            book = self.get_book()
        except(KeyError, Book.DoesNotExist):
            return HttpResponseRedirect(reverse('book:index'))
        return {
            'book': book
        }

    def form_valid(self, form):
        book = self.get_book()
        if 'edit' in self.request.POST:
            form.updateBook(book)
        return HttpResponseRedirect(reverse('book:book', args=(book.id,)))

    def get_success_url(self):
        return reverse('book:book', args=(self.kwargs['num']))

    def dispatch(self, request, *args, **kwargs):
        book = self.get_book()
        if book is None or not self.request.user.is_authenticated and book.user_id.id != self.request.user.id:
            return HttpResponseRedirect(reverse('book:index'))
        return super().dispatch(request, *args, **kwargs)

#This generic form view will create a book and add it to the database
class CreateBookView(generic.FormView):
    template_name = 'book/create.html'
    form_class = CreateBookForm #The form that the view will be based. It is located in forms.py
    success_url = '/'

    def form_valid(self, form):
        #This function will be called when the user will submit the form
        book = form.createBook(self.request.user)
        return HttpResponseRedirect(reverse('book:book', args=(book.id,)))

    def dispatch(self, request, *args, **kwargs):
        #This function is called before the page will be sent in order to verify if the user is authenticated
        #Otherwise, it will redirect it to the main page.
        if not self.request.user.is_authenticated:
            return HttpResponseRedirect(reverse('book:index'))
        return super().dispatch(request, *args, **kwargs)


# This view have the only purpose to delete a book from the database only if it is found. In all case, the page
# will be redirected to the main page (LibraryBook view).
def confirmDelete(request, num):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('book:index'))
    try:
        print('book id: ' + str(num))
        toReturn = Book.objects.get(pk=num)
        if toReturn.user_id.id != request.user.id:
            print('not allowed')
            return HttpResponseRedirect(reverse('book:index'))
        if request.method == 'POST':
            if 'delete' in request.POST:
                toReturn.delete()
                return HttpResponseRedirect(reverse('book:index'))
            if 'cancel' in request.POST:
                return HttpResponseRedirect(reverse('book:book', args=(toReturn.id,)))
        return render(request, 'book/delete.html', {
            'book': toReturn
        })
    except(KeyError, Book.DoesNotExist):
        print('does not exist')
        return HttpResponseRedirect(reverse('book:index'))
