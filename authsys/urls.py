from .views import *
from django.urls import path

urlpatterns = [
    path('create/', SignUpView.as_view(), name='create_user'),
    path('signin/', CustomLoginView.as_view(), name="signin"),
    path('logout/', logout, name="logout"),

]
