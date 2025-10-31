method_decorator() should preserve wrapper assignments

Description

the function that is passed to the decorator is a partial object and does not have any of the attributes expected from a function i.e. __name__, __module__ etc...
I have a logger decorator that wraps the target function to log its name, arguments and result. I applied it to a class method hello_world using method_decorator, instantiated the Test class, and invoked test_method(), expecting it to return "hello" and record a debug message.  
This results in the following exception  
AttributeError: 'functools.partial' object has no attribute '__name__'