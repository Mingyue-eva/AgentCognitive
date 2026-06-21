object HttpResponseNotAllowed can't be used in 'await' expression

Description

When defining a simple View subclass with only an async post method, any GET request made to that view causes the server to crash. Instead of returning a normal 405 Method Not Allowed response, the framework tries to await the response object and triggers a type error indicating that HttpResponseNotAllowed cannot be used in an await expression. The client sees a 500 Internal Server Error.

To reproduce this issue, set up a fresh Django 4.1.1 project running on Python 3.10.6. Add a view class that only implements an asynchronous handler for POST requests and register it at the URL path “/demo.” Start the development server and then open http://127.0.0.1:8000/demo in a browser (issuing a GET request). Instead of getting the expected 405 Method Not Allowed response, the server raises a type error during request processing and returns a 500 error.