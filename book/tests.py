from django.test import TestCase
from django.utils import timezone
from django.urls import reverse, reverse_lazy

from django.contrib.auth.models import User

from .models import Book, Wallet
from .forms import CreateBookForm


# This class contains a set of tests that will interact directly with the database
class DataBaseInteractionTests(TestCase):
    def setUp(self):
        user1 = User.objects.create(username="User1")
        user2 = User.objects.create(username="User2")
        Wallet.objects.create(balance=10.0, owner=user1)
        Wallet.objects.create(balance=5.0, owner=user2)
        Book.objects.create(title="BookOne", author="Bot1", publication_date=timezone.now(),
                            description="This book is a masterclass", gender="Cool", price=2.5, num_pages=500,
                            owner=user1)
        Book.objects.create(title="BookTwo", author="Bot2", publication_date=timezone.now(),
                            description="This book is okay but idc", gender="Not Cool", price=9.5, num_pages=200,
                            owner=user2)

    def test_plus(self):
        self.assertEqual(1 + 1, 2)

    # These three simple tests have the only purpose to test if basic database interaction works: Create, Edit and Delete.
    def test_create_book_form(self):
        form = CreateBookForm(
            data={"title": "Titre", "author": "Mires", "description": "best book", "gender": "Action", "num_pages": 15,
                  "price": 15.2})
        user = User.objects.get(username="User1")
        for user in User.objects.all():
            print(user.id)
        book = form.create_book(User.objects.get(username="User1"))
        self.assertIn(book, Book.objects.all())

    def test_edit_book(self):
        book = Book.objects.get(title="BookOne")
        book.price = 5
        book.save()
        self.assertEqual(Book.objects.get(title="BookOne").price, book.price)

    def test_delete_book(self):
        book = Book.objects.get(title="BookOne")
        book.delete()
        self.assertNotIn(book, Book.objects.all())

    # This test have the purpose to verify if the book buying process works
    def test_Buy(self):
        user = User.objects.get(pk=1)
        book = Book.objects.get(owner_id=2)
        wallet = Wallet.objects.get(owner_id=user.id)
        owner_wallet = Wallet.objects.get(owner_id=book.owner.id)
        self.assertGreater(wallet.balance, book.price)
        previous_buyer_balance = wallet.balance
        previous_owner_balance = owner_wallet.balance

        book.purchasers.add(user)
        wallet.balance -= book.price
        owner_wallet.balance += book.price
        wallet.save()
        owner_wallet.save()
        book.save()
        self.assertIn(user, book.purchasers.all())
        self.assertEqual(book.price + wallet.balance, previous_buyer_balance)
        self.assertEqual(owner_wallet.balance - book.price, previous_owner_balance)


# This class contains a set of tests that will verify the functionality of the views when the user is disconnected
class TestViews(TestCase):

    def setUp(self):
        user1 = User.objects.create(username="User1")
        Book.objects.create(title="BookOne", author="Bot1", publication_date=timezone.now(),
                            description="This book is a masterclass", gender="Cool", price=2.5, num_pages=500,
                            owner=user1)

    def test_owned_books_redirect(self):
        response = self.client.get(reverse('book:ownedBooks'))
        self.assertTemplateNotUsed(response, 'book/books.html')

    def test_purchased_books_redirect(self):
        response = self.client.get(reverse('book:purchasedBooks'))
        self.assertTemplateNotUsed(response, 'book/books.html')

    def test_shop(self):
        response = self.client.get(reverse('book:shop'))
        self.assertTemplateUsed(response, 'book/shop.html')
        self.assertIn(Book.objects.get(title="BookOne"), response.context['books'])

    def test_create_book_view(self):
        response = self.client.get(reverse('book:create'))
        self.assertTemplateNotUsed(response, 'book/create.html')

    def test_edit_book(self):
        response = self.client.get(reverse('book:edit', args=(1,)))
        self.assertTemplateNotUsed(response, 'book/edit.html')

    def test_delete_book(self):
        response = self.client.get(reverse('book:delete', args=(1,)))
        self.assertTemplateNotUsed(response, 'book/delete.html')


# This class contains a set of tests that will verify the functionality of the views when the user is logged-in
class TestViewsLogged(TestCase):
    def setUp(self):
        user = User.objects.create(username="User1")
        user.set_password("test123")
        user.save()
        self.client.login(username="User1", password="test123")

    def test_purchased_books_empty(self):
        response = self.client.get(reverse('book:purchasedBooks'))
        self.assertTemplateUsed(response, 'book/books.html')
        self.assertQuerysetEqual(response.context['library'], map(repr, []))

    def test_owned_books_empty(self):
        response = self.client.get(reverse('book:ownedBooks'))
        self.assertTemplateUsed(response, 'book/books.html')
        self.assertQuerysetEqual(response.context['library'], map(repr, []))

    def test_create_book(self):

        test = self.client.post(reverse('book:create'), {'title': 'Livre', 'author': 'Moi', 'description': 'Best seller', 'gender': 'Action', 'num_pages': 200, 'price': 6.5})
        print(test)
        livre = Book.objects.get(title="Livre")
        print(livre)

        # user = User.objects.get(username="User1")
        # book = form.create_book(user)
        # self.assertNotEqual(book, None)