sqrtdenest raises IndexError
When attempting to denest the expression (3 – sqrt(2)*sqrt(4 + 3*I) + 3*I)/2, the algorithm fails inside radsimp._split_gcd: it tries to access the first element of an empty tuple, causing an IndexError (“tuple index out of range”).
If an expression cannot be denested it should be returned unchanged.
IndexError fixed for sqrtdenest.
Fixes #12420
Now if the expression can’t be denested, it will be returned unchanged.

Old Result:
>>> sqrtdenest((3 - sqrt(2)*sqrt(4 + 3*I) + 3*I)/2)
IndexError: tuple index out of range

New Result:
In [9]: sqrtdenest((3 - sqrt(2)*sqrt(4 + 3*I) + 3*I)/2)
Out[9]: 3/2 - sqrt(2)*sqrt(4 + 3*I)/2 + 3*I/2