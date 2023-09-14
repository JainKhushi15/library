from django.http import JsonResponse
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .models import Book, Booking
from datetime import datetime, timedelta
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.views import APIView

# Create your views here.
@api_view(['POST'])
def registerUser(request):
    try:
        username = request.data['username']
        password = request.data['password']
        email = request.data['email']

        if User.objects.filter(email=email).exists():
            return JsonResponse({'status': 'Email is already registered', 'status_code': 400})

        user = User.objects.create_user(username=username, password=password, email=email)
        user.save()

        return JsonResponse({'status': 'Account successfully created', 'status_code': 200})
    
    except Exception as e:
        return JsonResponse({'status': 'Error creating account', 'status_code': 400})


@api_view(['POST'])
def loginUser(request):
    try:
        username = request.data['username']
        password = request.data['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            return JsonResponse({
                'status': 'Login successful',
                'status_code': 200,
                'user_id': user.id,
                
            })
        
        else:
            return JsonResponse({'Error'})
    
    except Exception as e:
        return JsonResponse({'message': 'Error adding the book', 'status_code': 400})
        
@api_view(['POST'])
# @permission_classes([IsAuthenticated])
def addNewBook(request):
    try:
        if request.user:
            title = request.data['title']
            author = request.data['author']
            isbn = request.data['isbn']

            book = Book(title=title, author=author, isbn=isbn)
            book.save()

            return JsonResponse({'message': 'Book added successfully', 'book_id': book.id})
        else:
            return JsonResponse({'message': 'Permission denied. Admin access required.', 'status_code': 403})
    except Exception as e:
        return JsonResponse({'message': 'Error adding the book', 'status_code': 400})
        
    
@api_view(['GET'])
def searchBooksByTitle(request):
    try:
        search_query = request.query_params.get('title', '')
        if search_query:
            books = Book.objects.filter(Q(title__icontains=search_query))
            book_list = [{'title': book.title, 'author': book.author, 'isbn': book.isbn} for book in books]
            return JsonResponse({'results': book_list})
        else:
            return JsonResponse({'results': []})
    except Exception as e:
        return JsonResponse({'message': 'Error searching for books', 'status_code': 500})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getBookAvailability(request, book_id):
    try:
        try:
            book = Book.objects.get(id=book_id)
        except ObjectDoesNotExist:
            return JsonResponse({'message': 'Book not found', 'status_code': 404})

        is_available = Booking.objects.filter(book=book, return_time__gte=datetime.now()).count() == 0

        if is_available:
            return JsonResponse({
                'book_id': book.id,
                'title': book.title,
                'author': book.author,
                'available': True
            })
        else:
            next_available_time = Booking.objects.filter(book=book, return_time__gte=datetime.now()).order_by('return_time').first().return_time
            return JsonResponse({
                'book_id': book.id,
                'title': book.title,
                'author': book.author,
                'available': False,
                'next_available_at': next_available_time
            })
    except Exception as e:
        return JsonResponse({'message': 'Error checking book availability', 'status_code': 500})


@api_view(['GET'])
def searchBooksByTitle(request):
    try:
        search_query = request.query_params.get('title', '')
        if search_query:
            books = Book.objects.filter(Q(title__icontains=search_query))
            book_list = [{'title': book.title, 'author': book.author, 'isbn': book.isbn} for book in books]
            return JsonResponse({'results': book_list})
        else:
            return JsonResponse({'results': []})
    except Exception as e:
        return JsonResponse({'message': 'Error searching for books', 'status_code': 500})

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def bookBook(request):
    try:
        book_id = request.data.get('book_id')
        issue_time = request.data.get('issue_time')
        return_time = request.data.get('return_time')

        book = Book.objects.get(id=book_id)
        if Booking.objects.filter(book=book, return_time__gte=datetime.now()).count() == 0:
            booking = Booking(user=request.user, book=book, issue_time=issue_time, return_time=return_time)
            booking.save()
            return JsonResponse({'status': 'Book booked successfully', 'status_code': 200})
        else:
            return JsonResponse({'status': 'Book is already booked', 'status_code': 400})
    except ObjectDoesNotExist:
        return JsonResponse({'status': 'Book not found', 'status_code': 404})
    except Exception as e:
        return JsonResponse({'status': 'Error booking the book', 'status_code': 500})