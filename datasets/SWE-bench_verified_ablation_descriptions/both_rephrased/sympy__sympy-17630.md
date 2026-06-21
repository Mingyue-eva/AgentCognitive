Exception when multiplying BlockMatrix containing ZeroMatrix blocks

A two-by-two block matrix is constructed so that its top-left submatrix is a symbolic 2×2 object and its other three submatrices are explicit zero matrices. When this block matrix is multiplied by itself once—either by using the high-level block collapse operation or by calling the internal block multiplication routine directly—the outcome is exactly as expected: the top-left block becomes the square of the symbolic matrix and every other block remains a zero matrix.

However, if the user multiplies the same block matrix three times in succession—whether by collapsing the expression b * b * b or by chaining two internal block multiplication calls—the process fails. At that point one of the zero blocks has been converted into a plain numeric zero value, and the multiplication logic then tries to query its column dimension. Because a bare zero does not have a cols attribute, an attribute error is raised.

This seems to be caused by the fact that the zeros in `b._blockmul(b)` are not `ZeroMatrix` but `Zero`:

```
>>> type(b._blockmul(b).blocks[0, 1])
<class 'sympy.core.numbers.Zero'>
```

However, I don't understand SymPy internals well enough to find out why this happens. I use Python 3.7.4 and sympy 1.4 (installed with pip).