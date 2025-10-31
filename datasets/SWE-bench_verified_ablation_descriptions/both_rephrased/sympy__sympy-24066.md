SI._collect_factor_and_dimension() cannot properly detect that exponent is dimensionless

How to reproduce:
First, form the ratio of the unit “second” to the product of “ohm” and “farad.” When this ratio is analyzed by the internal routine that separates numerical factors from physical dimensions, it correctly reports that the result is dimensionless. Next, create a new expression by adding a plain number (for example 100) to the exponential of that same ratio. Invoking the same analysis on this combined expression triggers the problem.

Runtime error:
When the routine examines the expression containing the exponential, it raises an exception because it believes the exponent carries a non-dimensionless unit (specifically time divided by capacitance times impedance), even though exponentials are supposed to accept only dimensionless arguments.