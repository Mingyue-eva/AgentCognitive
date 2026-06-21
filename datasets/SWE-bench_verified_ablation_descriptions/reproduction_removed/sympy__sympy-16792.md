autowrap with cython backend fails when array arguments do not appear in wrapped expr

When using the cython backend for autowrap, it appears that the code is not correctly generated when the function in question has array arguments that do not appear in the final expression. Calling the wrapped function on an array argument yields:

TypeError: only size-1 arrays can be converted to Python scalars

Inspection reveals that the corresponding C function is generated with an incorrect signature:

```C
double autofunc(double x) {
   double autofunc_result;
   autofunc_result = 1.0;
   return autofunc_result;
}
```

(`x` should be `double *`, not `double` in this case)

This error does not occur if the expression depends on each argument. One often needs functions to have a pre-defined signature regardless of whether a given argument contributes to the output.

I think I've identified the problem in `codegen` and will suggest a PR shortly.