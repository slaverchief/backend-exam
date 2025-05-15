from django.views import View
from django.shortcuts import redirect
from django.contrib import messages
from .models import BookSet


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