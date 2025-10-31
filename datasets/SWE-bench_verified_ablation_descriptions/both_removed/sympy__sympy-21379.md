Unexpected `PolynomialError` when using simple `subs()` for particular expressions

I am seeing weird behavior with `subs` for particular expressions involving hyperbolic sinusoids with piecewise arguments. Before using a TensorFlow lambdify, I was umbrella‐applying a casting from int to float of all int atoms to avoid potential TensorFlow type errors. Under certain conditions, applying `subs` raises an unexpected `PolynomialError`.

Sympy version: 1.8.dev

I am not really sure where the issue is, but I think it has something to do with the order of assumptions in this specific type of expression. Here is what I found–

- The error only happens with `cosh` or `tanh` in place of `sinh`; otherwise it succeeds.  
- The error goes away if removing the division by one of the symbols.  
- The error goes away if removing the outer `exp` (but it stays for most other unary functions like `sin` or `log`).  
- The error only happens when certain symbols have real assumptions.