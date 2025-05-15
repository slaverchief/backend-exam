from django.views.generic import ListView, View
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from main.models import Review
from django.urls import reverse_lazy
from django.shortcuts import render, get_object_or_404, redirect
from main.models import STATUSES


class UserReviewsListView(LoginRequiredMixin, ListView):
    model = Review
    template_name = 'review_management/user_reviews.html'
    context_object_name = 'reviews'
    paginate_by = 10
    login_url = reverse_lazy("signin")

    def get_queryset(self):
        return Review.objects.filter(
            user=self.request.user
        ).select_related('book').order_by('-date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Мои рецензии'
        return context


class ReviewModerationListView(UserPassesTestMixin, ListView):
    model = Review
    template_name = 'review_management/moder_reviews.html'
    context_object_name = 'reviews'
    paginate_by = 10

    def test_func(self):
        return self.request.user.is_staff or self.request.user.is_superuser

    def get_queryset(self):
        return Review.objects.filter(
            status=1  # На рассмотрении
        ).select_related('book', 'user').order_by('date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Модерация рецензий'
        return context


class ReviewModerationView(View):
    template_name = 'review_management/moder_reviews_detail.html'

    def get(self, request, pk):
        review = get_object_or_404(Review, id=pk)
        context = {
            'review': review,
            'statuses': STATUSES,
        }
        return render(request, self.template_name, context)

    def post(self, request, pk):
        review = get_object_or_404(Review, id=pk)
        action = request.POST.get('action')

        if action == 'approve':
            review.status = 3  # Одобрено
        elif action == 'reject':
            review.status = 2  # Отклонено

        review.save()
        return redirect('mod_reviews')