## Issue Description
Unexpected exception when multiplying geometry.Point and number
```python
from sympy import geometry as ge
import sympy

point1 = ge.Point(0,0)
point2 = ge.Point(1,1)
```

This line works fine
```python
point1 + point2 * sympy.sympify(2.0)
```

But when I write the same this way it raises an exception
```python
point1 + sympy.sympify(2.0) * point2
```

When attempting to add the expression `2.0*Point2D(1, 1)` to `Point(0, 0)`, Sympy’s addition logic tries to normalize dimensions by constructing a Point from the operand. Because it encounters a generic multiplication object (`Mul`) instead of a coordinate sequence, it cannot convert it into a Point and ultimately raises a GeometryError stating it doesn’t know how to add `2.0*Point2D(1, 1)` and a Point object.