import hashlib
import os
from django.contrib.auth.models import User

from django.db import models

class Book(models.Model):
    name = models.CharField(max_length=255)
    desc = models.TextField()
    year = models.IntegerField()
    madeby = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    amount = models.IntegerField()

    def get_color_reviews(self):
        mid = round(self.count_reviews())
        COLORS = {
            5: "green",
            4: "#c7ff24",
            3: "#ffdb24",
            2: "orange",
            1: "red"
        }
        return COLORS[mid]


    def count_reviews(self):
        amount = common = 0
        for review in self.reviews.all():
            amount+=1
            common += review.rate
        if amount == 0:
            return None
        return common/amount

class Genre(models.Model):
    name = models.CharField(max_length=255, unique=True)
    books = models.ManyToManyField(to=Book, related_name="genres", blank=True)

    def __str__(self):
        return self.name


class BookCover(models.Model):
    def upload_to(instance, filename):
        # Сохраняем в подпапках по MD5 (первые 2 символа)
        md5 = instance.md5
        return f'book_covers/{md5[:2]}/{md5}/{filename}'

    name = models.CharField(max_length=255)
    mimetype = models.CharField(max_length=255)
    md5 = models.CharField(max_length=32, unique=True)
    file = models.FileField(upload_to=upload_to)
    book = models.OneToOneField(to="Book", related_name="cover", on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        if not self.md5 and self.file:
            # Вычисляем MD5 только при первом сохранении
            self.file.seek(0)
            self.md5 = hashlib.md5(self.file.read()).hexdigest()
            self.file.seek(0)
            self.mimetype = self.file.file.content_type
            self.name = os.path.basename(self.file.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Обложка для {self.book.name}"

class Review(models.Model):
    book = models.ForeignKey("Book", on_delete=models.CASCADE, related_name="reviews")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rate = models.IntegerField()
    text = models.TextField()
    date = models.DateTimeField(auto_now=True)

    def get_rate_display(self):
        RATE_CHOICES = {
            5: 'Отлично',
            4: 'Хорошо',
            3: 'Удовлетворительно',
            2: 'Плохо',
            1: 'Ужасно'
        }
        return RATE_CHOICES.get(self.rate, '')

    def get_rate_color(self):
        RATE_CHOICES = {
            5: "green",
            4: "#c7ff24",
            3: "#ffdb24",
            2: "orange",
            1: "red"
        }
        return RATE_CHOICES.get(self.rate, '')
