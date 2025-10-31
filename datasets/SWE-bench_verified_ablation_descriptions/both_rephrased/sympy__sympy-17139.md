## Issue Description  
simplify(cos(x)**I): Invalid comparison of complex I (fu.py)

To reproduce this problem, open a Python session, import everything from SymPy, create a symbolic variable named x, and then attempt to simplify the expression cos(x) raised to the imaginary unit I. You would expect SymPy to return a simplified form of that expression.

Instead of yielding a valid result, the simplification routine fails when it tries to determine whether the exponent is negative. Because the exponent is the imaginary unit, comparing it to zero is not allowed, and this triggers a TypeError indicating that a complex value cannot be compared.