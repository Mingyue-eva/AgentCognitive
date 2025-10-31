method_decorator() should preserve wrapper assignments

Description

the function that is passed to the decorator is a partial object and does not have any of the attributes expected from a function i.e. __name__, __module__ etc...
consider the following case

Reproduction:
Define a decorator that wraps any callable to log its name, the arguments it was called with, and its return value. Apply this decorator to a method in a class using method_decorator. Instantiate the class and invoke the decorated method.

Expected Result:
The method should execute normally, return its expected value, and emit a log entry showing the method’s name, input arguments, and output.

Runtime Error:
When the decorated method is called, an AttributeError is raised because method_decorator passes a functools.partial object to the logging decorator. That partial object lacks the __name__ attribute, so the decorator’s attempt to read it fails.