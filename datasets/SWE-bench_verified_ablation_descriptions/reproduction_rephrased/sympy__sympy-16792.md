autowrap with cython backend fails when array arguments do not appear in wrapped expr

When using the cython backend for autowrap, it appears that the code is not correctly generated when the function in question has array arguments that do not appear in the final expression. For example, I created a 2×1 MatrixSymbol x in Sympy and wrapped the constant expression 1.0 with autowrap(expr, args=(x,), backend='cython'). Then I called the resulting function on a NumPy array for x. I expected it to return 1.0, but instead it fails with:

```python
TypeError: only size-1 arrays can be converted to Python scalars
```

A little inspection reveals that this is because the corresponding C function is generated with an incorrect signature:

```C
double autofunc(double x) {

   double autofunc_result;
   autofunc_result = 1.0;
   return autofunc_result;

}
```

(`x` should be `double *`, not `double` in this case)

If I modify the expression so that it actually depends on x—for instance by setting expr = x[0,0]—then autowrap produces the correct signature and calling the function with the same NumPy array returns 1.0 as expected, without failure.

I think I've identified the problem in `codegen` and will suggest a PR shortly.