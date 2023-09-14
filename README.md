HTTP Requests
##Admin:
http://127.0.0.1:8000/admin/

1. Register a User
http://127.0.0.1:8000/api/signup/

Example: 
{
    "username": "example_user",
    "password": "example_password",
    "email": "user@example.com"
}

2. Login User
http://localhost:8000/api/login/

Example:
{
    "username": "example_user",
    "password": "example_password"
}

3. Add a new book (admin endpoint)
http://127.0.0.1:8000/api/createBook/

Example:
{
    "title": "The Great Gatsby",
    "author": "F. Scott Fitzgerald",
    "isbn": "9781234567890"
}

4. Search books by title
http://localhost:8000/api/books/?title=The%20Great%20Gatsby

5. Book a book(Borrow)
http://127.0.0.1:8000/api/books/borrow/

Example:
{
    "book_id": "12345",
    "user_id": "123",
    "issue_time": "2023-01-02T12:00:00Z",
    "return_time": "2023-01-02T12:00:00Z"
}

