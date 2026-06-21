.subs on coth(log(tan(x))) errors for certain integral values

To reproduce the problem, import the SymPy library, declare x as a symbolic variable, and form the expression coth(log(tan(x))). Then substitute x with an integer value (for example, 2) and attempt to evaluate the result. In practice, you expect to get a numerical value after substitution.

Instead of a number, the evaluation step fails when dealing with certain integer inputs because the code refers to an internal name (“cotm”) that has not been defined. As a result, a NameError is raised during the hyperbolic function evaluation.

Fails for 2, 3, 5, 6, 8, 9, 11, 12, 13, 15, 18, … etc.