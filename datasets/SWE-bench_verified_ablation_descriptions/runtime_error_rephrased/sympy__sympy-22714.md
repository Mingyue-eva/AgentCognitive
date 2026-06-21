## Task Objective
You are given a software issue description that may include both:
1. Detailed reproduction steps or executable test code, along with the expected output.
2. Executable code that triggers a runtime error, including the corresponding error message or stack trace.

Your task is to rewrite **only** the runtime error-related portion — turning it into a natural language explanation that a human developer might give when describing what went wrong.

## Issue Description
simpify gives `Imaginary coordinates are not permitted.` with evaluate(False)

## Issue
`with evaluate(False)` crashes unexpectedly with `Point2D`

## Code
```python
import sympy as sp
with sp.evaluate(False):
  sp.S('Point2D(Integer(1),Integer(2))')
```

## Error
When running under `with evaluate(False)`, SymPy ends up calling the `Point2D` constructor in an unevaluated context, and this triggers a `ValueError` deep in `sympy/geometry/point.py` complaining that "Imaginary coordinates are not permitted."