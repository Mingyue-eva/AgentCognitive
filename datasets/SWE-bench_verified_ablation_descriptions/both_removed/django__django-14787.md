method_decorator() should preserve wrapper assignments

the function that is passed to the decorator is a partial object and does not have any of the attributes expected from a function i.e. __name__, __module__ etc.