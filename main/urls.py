from .views import *
from django.urls import path

urlpatterns = [
    path('create/', BookCreateView.as_view(), name='create_book'),
    path('delete/<int:bookid>', DeletionView.as_view(), name="delete_book"),
    path('detail/<int:pk>', BookDetailView.as_view(), name="detail"),
    path("review/<int:pk>", AddReviewView.as_view(), name="add_review"),
    path('edit/<int:pk>', BookUpdateView.as_view(), name="update_book"),
    path('', BookListView.as_view(), name='mainpage')
]
