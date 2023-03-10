from django import forms
from .models import Book
from django.utils import timezone

class EditBookForm(forms.Form):
    title = forms.CharField()
    author = forms.CharField()
    num_pages = forms.IntegerField()

    def updateBook(self, book):
        book.title = self.data['title']
        book.author = self.data['author']
        book.num_pages = self.data['num_pages']
        book.save()


class CreateBookForm(forms.Form):
    title = forms.CharField()
    author = forms.CharField()
    num_pages = forms.IntegerField()

    def createBook(self, user):
        now = timezone.now()
        book = Book(title=self.data['title'], author=self.data['author'], num_pages=self.data['num_pages'],
                    publication_date=now, user_id=user)
        book.save()
        return book

class SearchBookForm(forms.Form):
    titleSearched = forms.CharField()

    def levenshtein_ratio_and_distance(self, s, t):
        """ levenshtein_ratio_and_distance:
            Calculates levenshtein distance between two strings.
            If ratio_calc = True, the function computes the
            levenshtein distance ratio of similarity between two strings
            For all i and j, distance[i,j] will contain the Levenshtein
            distance between the first i characters of s and the
            first j characters of t
        """
        # Initialize matrix of zeros
        rows = len(s) + 1
        cols = len(t) + 1
        distance = [[0 for x in range(cols)] for y in range(rows)]

        # Populate matrix of zeros with the indeces of each character of both strings
        for i in range(1, rows):
            for k in range(1, cols):
                distance[i][0] = i
                distance[0][k] = k

        # Iterate over the matrix to compute the cost of deletions,insertions and/or substitutions
        for col in range(1, cols):
            for row in range(1, rows):
                if s[row - 1] == t[col - 1]:
                    cost = 0  # If the characters are the same in the two strings in a given position [i,j] then the cost is 0
                else:
                    # In order to align the results with those of the Python Levenshtein package, if we choose to calculate the ratio
                    # the cost of a substitution is 2. If we calculate just distance, then the cost of a substitution is 1.
                    cost = 2
                distance[row][col] = min(distance[row - 1][col] + 1,  # Cost of deletions
                                         distance[row][col - 1] + 1,  # Cost of insertions
                                         distance[row - 1][col - 1] + cost)  # Cost of substitutions
            # Computation of the Levenshtein Distance Ratio
        return ((len(s) + len(t)) - distance[row][col]) / (len(s) + len(t))

    def valid_book(self, title):
        value = self.levenshtein_ratio_and_distance(title, self.data['titleSearched'])
        return value > 0.8

    def search_books(self):
        books = Book.objects.all()
        newList = []
        for book in books:
            if self.valid_book(book.title):
                newList.append(book)
        return newList
