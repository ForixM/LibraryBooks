from django.views import generic
from .models import Book
from django.shortcuts import render, HttpResponseRedirect, reverse
from django.utils import timezone

#The main page view. All books that are stored in the database will be returned as a queryset usable in the HTML code.
class LibraryBook(generic.ListView):
    template_name = "book/index.html"
    context_object_name = "library"
    def get_queryset(self):
        return Book.objects.all()

#This view have a form to edit book informations in the database
def editBook(request, num):
    #Used to retrieve the book in the database. An error will be raised if the book don't exists
    book = Book.objects.get(pk=num)
    try:
        #These three variables will retrieve the content of the inputs elements
        in1 = request.POST['in1']
        in2 = request.POST['in2']
        in3 = request.POST['in3']
    except (KeyError, Book.DoesNotExist):
        return render(request, 'book/edit.html', {
            "title": book.title,
            "author": book.author,
            "num_pages": book.num_pages,
            "id": num,
        })
    else:
        #The book will be updated regarding the three variables (in1, in2, in3) retrieved previously
        book.title = in1
        book.author = in2
        book.num_pages = in3
        book.save()
        #The page will be redirected to the updated book informations view (book:book)
        return HttpResponseRedirect(reverse('book:book', args=(num,)))

#This view has a form in order to create a book.
def createBook(request):
    try:
        #The three text inputs in the HTML file will have their content retrieved into these three variables
        in1 = request.POST['in1']
        in2 = request.POST['in2']
        in3 = request.POST['in3']
    except (KeyError, Book.DoesNotExist):
        return render(request, 'book/create.html', {
            "test": Book()
        })
    else:
        #A new book will be created and saved in the database. timezone will be used to set the creation date of the book
        #at the time it will be inserted into the database. After that, the page will be redirected to the main page
        now = timezone.now()
        newBook = Book(title=in1, author=in2, publication_date=now, num_pages=int(in3))
        newBook.save()
        return HttpResponseRedirect(reverse('book:index'))

#This view will retrieve the book id from the url, and tries to find it in the database.
#If the book exists in the database, the view with the book informations will be displayed.
#Otherwise, the page will be automatically redirected to the main page (LibraryBook view).
def book(request, num):
    try:
        toReturn = Book.objects.get(pk=num)
        return render(request, 'book/book.html', {
            'book': toReturn,
            'bookId': toReturn.id
        })
    except(KeyError, Book.DoesNotExist):
        return HttpResponseRedirect(reverse('book:index'))

#This view have the only purpose to delete a book from the database only if it is found. In all case, the page
#will be redirected to the main page (LibraryBook view).
def confirmDelete(request, num):
    try:
        toReturn = Book.objects.get(pk=num)
        toReturn.delete()
    except(KeyError, Book.DoesNotExist):
        return HttpResponseRedirect(reverse('book:index'))
    return HttpResponseRedirect(reverse('book:index'))