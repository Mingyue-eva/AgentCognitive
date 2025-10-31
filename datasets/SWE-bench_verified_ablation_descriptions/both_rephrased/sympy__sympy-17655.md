## Issue Description
Unexpected exception when multiplying geometry.Point and number

In my test case I import SymPy’s geometry module and create two points: one at (0, 0) and one at (1, 1). When I multiply the second point by 2.0 and then add it to the first point, everything works as expected and I get a new point at (2, 2). However, if I write the multiplication with the scalar on the left (that is, 2.0 times the point) and then add that result to the first point, the operation fails.

At that moment a GeometryError is raised during the point‐addition routine because the library does not recognize the product of a floating-point number and a point as a valid point for addition. The internal logic cannot normalize the operands and therefore reports that it doesn’t know how to add those two objects.

The expected behaviour is, that both lines give the same result