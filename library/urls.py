from django.urls import path
from library.views import (registerUser, addNewBook, searchBooksByTitle, bookBook)
from . import views
urlpatterns = [
    # User registration
    path('signup/', views.registerUser, name='register_user'),

    # User login
    path('login/', views.loginUser, name='login_user'),

    # Add a new book (admin endpoint)
    path('createBook/', views.addNewBook, name='add_new_book'),

    # Search books by title
    path('books/', views.searchBooksByTitle, name='search_books_by_title'),

    # Get book availability
    path('books/<int:book_id>/availability/', views.getBookAvailability, name='get_book_availability'),

    # Book a book
    path('books/borrow/', views.bookBook, name='book_book'),
]