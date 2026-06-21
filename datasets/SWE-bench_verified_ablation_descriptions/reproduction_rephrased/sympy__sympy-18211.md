## Issue Description
`solveset` raises `NotImplementedError` instead of returning `ConditionSet`

The problem is  
When you ask Sympy to convert the equation n⋅cos(n) − 3⋅sin(n) = 0 into a solution set by calling `as_set()`, it raises
```
---------------------------------------------------------------------------
NotImplementedError
```
Here `solveset` raises `NotImplementedError` but probably a `ConditionSet` should be returned by `solveset` instead. You would expect it to return a `ConditionSet` representing all real solutions of the equation, i.e. the set of n ∊ ℝ satisfying n⋅cos(n) − 3⋅sin(n) = 0.

_Originally posted by @oscarbenjamin in https://github.com/sympy/sympy/pull/17771_