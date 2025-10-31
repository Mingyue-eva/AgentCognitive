## Issue Description
simplify(cos(x)**I): Invalid comparison of complex I (fu.py)

>>> from sympy import *
>>> x = Symbol('x')
>>> print(simplify(cos(x)**I))

During the simplification process, Sympy reaches a step where it tests whether the exponent I is less than zero. Because I is the imaginary unit (a complex number) and Python does not support ordering comparisons on complex values, this triggers a TypeError reporting “Invalid comparison of complex I.”