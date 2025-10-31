## Issue Description
SI._collect_factor_and_dimension() cannot properly detect that exponent is dimensionless

How to reproduce:
First, import the exponential function and the SI unit definitions from Sympy. Then create an expression for one second divided by the product of an ohm and a farad, and verify that SI._collect_factor_and_dimension reports it as dimensionless. Next, form a new expression by adding 100 to the exponential of that unit expression and call SI._collect_factor_and_dimension on it.

# results in ValueError: Dimension of "exp(second/(farad*ohm))" is Dimension(time/(capacitance*impedance)), but it should be Dimension(1)