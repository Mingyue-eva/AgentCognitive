## Issue Description
TemplateView.get_context_data()'s kwargs returns SimpleLazyObjects that causes a crash when filtering.  
Description

I have a view named OfferView that inherits from Django’s TemplateView and uses the "offers/offer.html" template. In Django 3.0, my get_context_data method simply pulled the offer_slug from kwargs (defaulting to an empty string) and passed it straight to get_object_or_404 to look up the Account by slug, which worked fine. After upgrading to Django 3.1, doing the exact same thing led to a runtime error, so I had to explicitly convert the value returned by kwargs.get("offer_slug", "") into a string before handing it off to get_object_or_404. My URLconf registers this view under the pattern '/offers/<slug:offer_slug>/' with the name "offer_view."

The error generated if you don't is:
Error binding parameter 0 - probably unsupported type  
from django/db/backends/sqlite3/operations.py, line 144, in _quote_params_for_last_executed_query

When debugging, I found that offer_slug (coming in from kwargs.get) was of type 'SimpleLazyObject' in Django 3.1, and when I explicitly converted it to a string, get_object_or_404 behaved as expected.  
This is using Python 3.7.8 with SQLite.