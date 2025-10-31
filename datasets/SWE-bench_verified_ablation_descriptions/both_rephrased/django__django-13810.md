Description

I experienced strange issues when working with ASGI, django-debug-toolbar and my own small middleware. It was hard problem to debug, I uploaded an example project here: https://github.com/hbielenia/asgi-djangotoolbar-bug (the name is misleading - I initially thought it's a bug with django-debug-toolbar).

Reproduction

In the example project, the session file path is intentionally set to a nonexistent location so that every request will fail when trying to store session data. If you start the application under Daphne and then navigate to the /admin URL, the request does not render the usual configuration error page or debug toolbar output. Instead, it triggers an unexpected failure before the error page can be displayed.

Error encountered

During this request, the middleware chain ends up invoking the response as though it were an asynchronous coroutine. Because the response object is not awaitable, a type error is raised at that point. If you disable the DummyMiddleware, the application falls back to its normal behavior and raises the expected configuration exception.

I’m not sure about the overall role of django-debug-toolbar here—removing it causes Daphne to return a 500 error page without debug information and no traceback in the console. I decided to leave it since it helped me approximate the causes of the issue.

I notice that in https://github.com/django/django/blob/3.1.4/django/core/handlers/base.py#L58 while MiddlewareNotUsed causes the loop to skip further processing and go to the next middleware, it does leave the handler variable overwritten with the output of self.adapt_method_mode(). On the next pass, this handler is passed to the next middleware instance, disregarding all the previous checks for (lack of) async support. This likely causes the middleware chain to be “poisoned” from this point onwards, resulting in the last middleware in the response cycle returning an HttpResponse as a synchronous middleware would, instead of a coroutine that is expected.

This is probably avoided by adding async support to my middleware, but unless I’m missing something the docs indicate it should work as it is. It is my intention that it’s applied only on synchronous requests, so I didn’t make it async compatible on purpose. If it’s intentional in Django that every middleware needs to support async when the application is run as an ASGI app, the documentation should probably state that clearly. Though it kind of defeats the purpose of having async_capable = False flag in the first place.