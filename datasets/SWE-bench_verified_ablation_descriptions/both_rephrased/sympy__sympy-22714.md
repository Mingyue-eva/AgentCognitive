## Issue Description
simpify gives `Imaginary coordinates are not permitted.` with evaluate(False)

## Issue
`with evaluate(False)` crashes unexpectedly with `Point2D`

Reproduction
To reproduce the problem, start a Python session, import sympy as sp, and enter a context where automatic evaluation is disabled by using `with sp.evaluate(False)`. Inside that block, call `sp.S` on the string `Point2D(Integer(1),Integer(2))`. You would expect this to produce a `Point2D` object with coordinates (1, 2).

Runtime error
Instead of producing a `Point2D` object, Sympy raises an error stating that imaginary coordinates are not permitted, even though both coordinates are real integers. This error only appears when evaluation is turned off; with evaluation enabled, the same input is parsed correctly.

However, it works without `with evaluate(False)`. Both of following commands work
```python
sp.S('Point2D(Integer(1),Integer(2))')
sp.S('Point2D(Integer(1),Integer(2))', evaluate=False)
```