## Issue Description  
`solveset` raises `NotImplementedError` instead of returning `ConditionSet`

To reproduce the problem, you form the symbolic equation n·cos(n) − 3·sin(n) = 0 and then ask Sympy to convert that equation into a set of solutions.  Rather than returning a description of the solution set, the library throws a NotImplementedError at that point.

We would expect the method to return a ConditionSet object describing all real numbers n that satisfy n·cos(n) − 3·sin(n) = 0, for example:

```julia
In [11]: ConditionSet(n, Eq(n*cos(n) - 3*sin(n), 0), Reals)  
Out[11]: {n | n ∊ ℝ ∧ n⋅cos(n) - 3⋅sin(n) = 0}
```

Here `solveset` raises `NotImplementedError` but probably a `ConditionSet` should be returned by `solveset` instead.

_Originally posted by @oscarbenjamin in https://github.com/sympy/sympy/pull/17771_