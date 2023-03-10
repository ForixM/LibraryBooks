from django.db import models
from django.contrib.auth.models import User


# This is the model that will structure how book information will be saved in the database.
class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    test = models.Field
    publication_date = models.DateTimeField('date published')
    num_pages = models.IntegerField()
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return "{ title=(" + str(self.title) + "), author=(" + str(self.author) + ", num_pages=(" + str(
            self.num_pages) + "), publication_date=(" + str(self.publication_date) + ")}"


# This model will store the wallet information of each user to give them the capability to buy books from the store
class Wallet(models.Model):
    balance = models.FloatField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return "account=" + str(self.owner) + ", balance=" + str(self.balance)
