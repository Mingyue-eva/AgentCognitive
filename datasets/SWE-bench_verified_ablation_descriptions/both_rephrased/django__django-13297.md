TemplateView.get_context_data()'s kwargs returns SimpleLazyObjects that causes a crash when filtering.

Description

To reproduce this issue, define a view by subclassing TemplateView and override its method for building the template context. In that method, read a parameter called offer_slug from the view’s keyword arguments and use it immediately to look up an Account record by its slug. Hook this view up to a URL pattern that captures offer_slug as a slug in the path. In Django 3.0, pulling offer_slug straight from kwargs and passing it to the lookup returns the correct object and the page renders normally.

At runtime in Django 3.1, the value you get from kwargs is not a plain string but a SimpleLazyObject. Passing that lazy object into the database lookup causes SQLite to reject the parameter because it cannot bind the unsupported type. If you convert the lazy object to a regular string before looking up the Account, the lookup succeeds and the view behaves as expected.

This was observed under Python 3.7.8 with an SQLite backend.