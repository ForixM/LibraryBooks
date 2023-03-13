from django.db import models
from django.contrib.auth.models import User


# This is the model that will structure how book information will be saved in the database.
class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    test = models.Field
    publication_date = models.DateTimeField('date published')
    num_pages = models.IntegerField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='related_primary_manual_roats')
    description = models.CharField(max_length=1000)
    gender = models.CharField(max_length=50)
    price = models.FloatField()

    # ManyToManyField behave like a list. It will store a queryset of foreign key of User to know which user purchased
    # the book.
    purchasers = models.ManyToManyField(User, related_name='related_secondary_manual_roats')


# This model will store the wallet information of each user to give them the capability to buy books from the store
class Wallet(models.Model):
    balance = models.FloatField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
