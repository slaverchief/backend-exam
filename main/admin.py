from django.contrib import admin
from .models import *

admin.site.register(Book)
admin.site.register(BookCover)
admin.site.register(Genre)
admin.site.register(Review)