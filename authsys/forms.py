from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

ROLE_CHOICES = [
    ('user', 'Обычный пользователь'),
    ('staff', 'Модератор'),
    ('admin', 'Администратор'),
]


class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(required=True, label="Имя")
    last_name = forms.CharField(required=True, label="Фамилия")
    role = forms.ChoiceField(
        choices=ROLE_CHOICES,
        label="Роль пользователя",
        widget=forms.Select(attrs={'class': 'role-select'})
    )

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'role', 'password1', 'password2')


    def save(self, commit=True):
        user = super().save(commit=False)
        role = self.cleaned_data['role']

        if role == 'staff':
            user.is_staff = True
            user.is_superuser = False
        elif role == 'admin':
            user.is_staff = True
            user.is_superuser = True
        else:
            user.is_staff = False
            user.is_superuser = False

        if commit:
            user.save()
        return user