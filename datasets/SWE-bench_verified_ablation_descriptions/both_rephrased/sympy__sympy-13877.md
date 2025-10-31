Matrix determinant raises Invalid NaN comparison with particular symbolic entries

To reproduce the issue, build an n×n matrix whose entry in row j and column i is given by i plus a times j, where a is a symbolic parameter and the indices run from 0 to n−1. Compute its determinant for successive values of n. The observed results are:
- For n = 1, the determinant is 0.
- For n = 2, the determinant simplifies to –a.
- For n = 3, the determinant expands to the polynomial 2·a·(a + 2) + 2·a·(2·a + 1) – 3·a·(2·a + 2).
- For n = 4, the determinant is 0.
- For n = 5, the computation returns NaN.

Expected behavior: each determinant should simplify to a meaningful symbolic expression rather than producing NaN.

When attempting the same determinant calculation at n = 6, the algorithm fails with an error indicating that an invalid comparison with NaN occurred during the factorization or simplification phase. This stops the determinant routine from completing.

Correct me if I’m wrong but isn’t the Bareiss algorithm only valid for integer matrices, which cannot be assumed here?