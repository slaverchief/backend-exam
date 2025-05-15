from django.db import models
from django.contrib.auth.models import User
from main.models import Book

class BookSet(models.Model):
    name = models.CharField(max_length=255)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    books = models.ManyToManyField(Book, related_name="booksets", blank=True)

