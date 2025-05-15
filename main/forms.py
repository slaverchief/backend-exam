from django import forms
from .models import Book, Genre, BookCover
import hashlib
import os


class BookCreateForm(forms.ModelForm):
    genres = forms.ModelMultipleChoiceField(
        queryset=Genre.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="Жанры"
    )
    cover = forms.FileField(
        required=False,
        label="Обложка книги",
        help_text="Загрузите изображение обложки"
    )

    class Meta:
        model = Book
        fields = ['name', 'desc', 'year', 'madeby', 'author', 'amount', 'genres']
        widgets = {
            'year': forms.NumberInput(attrs={'min': 1000, 'max': 2100}),
            'amount': forms.NumberInput(attrs={'min': 1}),
            'desc': forms.Textarea(attrs={'rows': 5}),
        }

    def save(self, commit=True):
        book = super().save(commit=True)
        cover_file = self.cleaned_data.get('cover')
        book.genres.set(self.cleaned_data.get('genres'))
        if cover_file:
            # Удаляем старую обложку, если есть
            if hasattr(book, 'cover'):
                book.cover.delete()

            # Создаем новую обложку
            md5 = hashlib.md5(cover_file.read()).hexdigest()
            cover_file.seek(0)

            BookCover.objects.create(
                name=cover_file.name,
                mimetype=cover_file.content_type,
                md5=md5,
                file=cover_file,
                book=book
            )

        return book

class BookEditForm(forms.ModelForm):
    genres = forms.ModelMultipleChoiceField(
        queryset=Genre.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="Жанры"
    )
    def save(self, commit=True):
        book = super().save(commit=True)
        book.genres.set(self.cleaned_data.get('genres'))
        return book

    class Meta:
        model = Book
        fields = ['name', 'desc', 'year', 'madeby', 'author', 'amount', 'genres']
        widgets = {
            'year': forms.NumberInput(attrs={'min': 1000, 'max': 2100}),
            'amount': forms.NumberInput(attrs={'min': 1}),
            'desc': forms.Textarea(attrs={'rows': 5}),
        }