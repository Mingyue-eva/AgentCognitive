SelectDateWidget can crash with OverflowError.

Description

Given a relatively common view like this:
from django import forms
from django.forms import SelectDateWidget
from django.http import HttpResponse
class ReproForm(forms.Form):
    my_date = forms.DateField(widget=SelectDateWidget())
def repro_view(request):
    form = ReproForm(request.GET)  # for ease of reproducibility
    if form.is_valid():
        return HttpResponse("ok")
    else:
        return HttpResponse("not ok")
# urls.py
urlpatterns = [path('repro/', views.repro_view, name='repro')]

To reproduce the problem, run the Django development server locally and send a GET request to the repro endpoint with valid day and month values but supply an extremely large number for the year parameter. Instead of returning a normal response, the server crashes. You can observe the same failure when submitting the form via POST with equivalent data.

During form validation, the SelectDateWidget takes the submitted strings, converts them into integers, and attempts to construct a date object. When one of those integers—typically the year—is larger than the platform’s maximum integer size, Python cannot convert it into a C long and raises an overflow error. This error bubbles up without being caught, causing an unhandled exception at the point where the code does:
    date_value = datetime.date(int(y), int(m), int(d)) 

Specifically, supplying an integer larger than sys.maxsize to datetime.date triggers an OverflowError indicating that the value is too large to convert to a C long.