Result from clear_denoms() prints like zero poly but behaves wierdly (due to unstripped DMP)  
The was the immediate cause of the ZeroDivisionError in #17990.

To reproduce this issue, start with a rather complicated constant expression built from cube roots, square roots, and integer coefficients that in fact simplifies to zero. Wrap that expression as a univariate polynomial and invoke the routine that clears denominators. Although the expression is zero, the clearing‐denominators routine returns a nontrivial coefficient representing the combined denominator and a polynomial object that prints exactly like the zero polynomial. However, that polynomial object does not behave as a true zero polynomial internally: its built‐in zero check reports false until you convert it back into a symbolic expression and check again, at which point it correctly evaluates to zero.

~~There may be valid cases (at least with EX coefficients) where the two valued Poly.is_zero is False but as_expr() evaluates to 0~~ (@jksuom points out this is a bug in #20428), but other Poly methods don't handle `bad_poly` very well.

When you attempt to compute the greatest‐common‐divisor of exponents on this malformed polynomial, the routine presumes at least one monomial is present and ends up indexing into an empty list, causing an out‐of‐range error. Likewise, in earlier versions of the library, invoking the routine that computes the polynomial’s content and primitive part would perform a division by zero during polynomial division, raising a zero‐division error.

Looking at the underlying DMP, there is an unstripped leading 0 in the list representation of the Poly

```
>>> bad_poly.rep
DMP([EX(0)], EX, None)
```

which should be

```
>>> Poly(0, x, domain="EX").rep
DMP([], EX, None)
```