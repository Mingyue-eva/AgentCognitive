MiddlewareNotUsed leaves undesired side effects when loading middleware in ASGI context  
Description  
I experienced strange issues when working with ASGI, django-debug-toolbar and my own small middleware.  

TypeError: object HttpResponse can't be used in 'await' expression  

I notice that in https://github.com/django/django/blob/3.1.4/django/core/handlers/base.py#L58 while MiddlewareNotUsed causes the loop to skip further processing and go to next middleware, it does leave handler variable overwritten with output of self.adapt_method_mode(). On next pass, this handler is passed to next middleware instance, disregarding all the previous checks for (lack of) async support. This likely causes the middleware chain to be "poisoned" from this point onwards, resulting in last middleware in response cycle to return an HttpResponse as a synchronous middleware would, instead of coroutine that is expected.  

This is probably avoided by adding async support to my middleware, but unless I'm missing something docs indicate it should work as it is. It is my intention that it's applied only on synchronous requests, so I didn't make it async compatible on purpose. If it's intentional in Django that every middleware needs to support async if the application is run as ASGI app, the documentation should probably state that clearly. Though it kinda defeats the purpose of having async_capable = False flag in the first place.