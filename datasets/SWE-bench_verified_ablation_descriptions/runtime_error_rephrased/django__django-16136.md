object HttpResponseNotAllowed can’t be used in ‘await’ expression

Description

When defining a simple View subclass with only an async post method, issuing a GET request to that view causes Django to return a 500 error. Under the hood, Django generates an HttpResponseNotAllowed for the unsupported GET, but because the view is async Django tries to await that response object. Since HttpResponseNotAllowed isn’t awaitable, a TypeError is thrown stating that the HttpResponseNotAllowed object can’t be used in an ‘await’ expression.

This can be easily reproduced with an empty project (no external dependencies) started with Django 4.1.1 and Python 3.10.6.

Basic view to reproduce the bug:
from django.views import View
from django.http import HttpResponse

class Demo(View):
    """This basic view supports only POST requests"""
    async def post(self, request):
        return HttpResponse("ok")

URL pattern to access it:
from django.urls import path
from views import Demo

urlpatterns = [
    path("demo", Demo.as_view()),
]

Start the local dev server (manage.py runserver) and open http://127.0.0.1:8000/demo in the browser. The server crashes with a 500 error as described above.