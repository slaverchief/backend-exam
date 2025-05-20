from django.http import HttpResponse

from django.views import View
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib import messages
from .models import BookSet
from django.db import models
from main.models import Book

# View для создания подборки
class CreateBookSetView(View):
    def post(self, request):
        if not request.user.is_authenticated:
            messages.error(request, "Необходимо авторизоваться")
            return redirect('mainpage')

        name = request.POST.get('name')
        if name:
            BookSet.objects.create(
                name=name,
                author=request.user
            )
            messages.success(request, "Подборка успешно создана")
        else:
            messages.error(request, "Название подборки не может быть пустым")

        return redirect('mainpage')

# View для просмотра страницы списка подборок
class UserBooksetsView(View):
    template_name = 'booksets/user_booksets.html'

    def get(self, request):
        if not request.user.is_authenticated:
            return redirect('signin')

        booksets = BookSet.objects.filter(author=request.user).annotate(
            book_count=models.Count('books')
        )

        context = {
            'booksets': booksets
        }
        return render(request, self.template_name, context)

# View для просмотра конкретной подборки
class BooksetDetailView(View):
    template_name = 'booksets/bookset_detail.html'

    def get(self, request, pk):
        bookset = get_object_or_404(BookSet, id=pk, author=request.user)
        books = bookset.books.all()

        context = {
            'bookset': bookset,
            'books': books
        }
        return render(request, self.template_name, context)

# View для добавления книги в подборку
class AddBookToBooksetView(View):
    def post(self, request, pk):
        if request.user.is_staff or request.user.is_superuser:
            return redirect('book_detail', book_id=pk)

        book = get_object_or_404(Book, id=pk)
        bookset_id = request.POST.get('bookset_id')

        try:
            bookset = BookSet.objects.get(id=bookset_id, author=request.user)
            bookset.books.add(book)
            messages.success(request, f"Книга добавлена в подборку '{bookset.name}'")
        except BookSet.DoesNotExist:
            messages.error(request, "Ошибка: подборка не найдена")

        return HttpResponse()