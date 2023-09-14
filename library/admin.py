from django.contrib import admin
from library.models import User, Book, Booking

# Register your models here.
admin.site.register(Book)
admin.site.register(Booking)