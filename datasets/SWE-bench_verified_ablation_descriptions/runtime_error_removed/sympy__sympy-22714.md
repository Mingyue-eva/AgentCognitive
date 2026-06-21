## Issue Description
simpify gives `Imaginary coordinates are not permitted.` with `evaluate(False)`

## Issue
`with evaluate(False)` crashes unexpectedly with `Point2D`

## Code
```python
import sympy as sp
with sp.evaluate(False):
    sp.S('Point2D(Integer(1),Integer(2))')
```

## Expected Behavior
It works without `with evaluate(False)`. Both of the following commands work:
```python
sp.S('Point2D(Integer(1),Integer(2))')
sp.S('Point2D(Integer(1),Integer(2))', evaluate=False)
```