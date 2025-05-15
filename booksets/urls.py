from .views import *
from django.urls import path

urlpatterns = [
    path('create/', CreateBookSetView.as_view(), name='create_bookset'),
]
