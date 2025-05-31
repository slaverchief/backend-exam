from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, View, DetailView, UpdateView
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .forms import *
from django.shortcuts import redirect, get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from .models import *
from django.core.paginator import Paginator


def is_superuser(request):
    if not request.user.is_superuser:
        messages.error(request, "Вы не имеете право на это действие")
        return False
    return True

# View для страницы списка книг
class BookListView(ListView):
    ListView.template_name = "main/listpage.html"
    ListView.model = Book
    ListView.context_object_name = "books"
    ListView.paginate_by = 10

# View для страницы конкретной книги
class BookDetailView(DetailView):
    model = Book
    template_name = 'main/book_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        book = self.object

        # Получаем рецензии с пагинацией
        reviews_list = Review.objects.filter(book=book).order_by('-date')
        paginator = Paginator(reviews_list, 10)
        page = self.request.GET.get('page')
        reviews = paginator.get_page(page)

        # Проверяем, есть ли у текущего пользователя рецензия
        user_review = None
        if self.request.user.is_authenticated:
            user_review = Review.objects.filter(book=book, user=self.request.user).first()

        context.update({
            'reviews': reviews,
            'user_review': user_review,
        })
        return context

# View для добавление рецензии
class AddReviewView(LoginRequiredMixin, CreateView):
    model = Review
    fields = ['rate', 'text']

    def form_valid(self, form):
        book = get_object_or_404(Book, pk=self.kwargs['pk'])
        form.instance.book = book
        form.instance.user = self.request.user
        print(form.cleaned_data)
        form.cleaned_data['text'] = form.cleaned_data['text'].strip()
        messages.success(self.request, 'Ваша рецензия добавлена!')
        return super().form_valid(form)


    def get_success_url(self):
        return reverse_lazy('detail', kwargs={'pk': self.kwargs['pk']})

# View для создания книги
class BookCreateView(CreateView):
    model = Book
    form_class = BookCreateForm
    template_name = 'main/creation.html'
    success_url = reverse_lazy('mainpage')
    login_url = reverse_lazy("signin")

    def dispatch(self, request, *args, **kwargs):
        sflag= is_superuser(request)
        if not sflag:
            return redirect("mainpage")
        return super().dispatch(request, *args, **kwargs)


    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, f'Книга "{form.instance.name}" успешно добавлена!')
        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Добавить книгу'
        return context

# View для страницы редактирования книги
class BookUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Book
    form_class = BookEditForm
    template_name = 'main/edit.html'

    def test_func(self):
        return self.request.user.is_staff or self.request.user.is_superuser

    def get_success_url(self):
        return reverse_lazy('mainpage')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Редактирование {self.object.name}'
        return context

# View для удаления книги
class DeletionView(View):

    def dispatch(self, request, *args, **kwargs):
        sflag= is_superuser(request)
        if not sflag:
            return redirect("mainpage")
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, bookid):
        try:
            Book.objects.get(pk=bookid).delete()
        except ObjectDoesNotExist:
            messages.error(request, "Нет такого объекта")
        return redirect("mainpage")
