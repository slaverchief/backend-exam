from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import user_passes_test
from .forms import *
from django.views.generic import CreateView
from django.contrib import messages
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect
from django.contrib.auth import logout as lg

# Функция, проверяющая, является ли пользователь суперпользователем
def is_superuser(user):
    return user.is_superuser

# View для регистрации
@method_decorator(user_passes_test(is_superuser), name='dispatch')
class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    template_name = "authsys/create_user.html"
    success_url = reverse_lazy('mainpage')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(
            self.request,
            f'Пользователь {form.instance.username} успешно создан'
        )
        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Создание пользователя'
        return context




# View для входа
class CustomLoginView(LoginView):
    template_name = 'authsys/signin.html'

    def get_success_url(self):
        return reverse_lazy("mainpage")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Авторизация'
        return context

    def form_invalid(self, form):
        messages.error(self.request, 'Неверное имя пользователя или пароль')
        return super().form_invalid(form)

def logout(request):
    lg(request)
    return redirect("mainpage")