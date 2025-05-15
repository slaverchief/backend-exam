from .views import *
from django.urls import path

urlpatterns = [
    path('create/', CreateBookSetView.as_view(), name='create_bookset'),
    path('list/', UserBooksetsView.as_view(), name="user_booksets"),
    path('detail/<int:pk>', BooksetDetailView.as_view(), name="bookset_detail"),
    path('add/<int:pk>', AddBookToBooksetView.as_view(), name="add_book_to_bookset")
]
