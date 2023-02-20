from django.db import models

#This is the model that will structure how book information will be saved in the database.
class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    publication_date = models.DateTimeField('date published')
    num_pages = models.IntegerField()
    def __str__(self):
        return "{ title=("+self.title+"), author=("+self.author+", num_pages=("+self.num_pages+"), publication_date=("+self.publication_date+")}"
