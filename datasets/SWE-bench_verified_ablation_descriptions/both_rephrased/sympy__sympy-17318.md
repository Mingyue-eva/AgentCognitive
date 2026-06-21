sqrtdenest raises IndexError

Reproduction
To reproduce this issue, invoke sqrtdenest on the complex expression consisting of three minus the product of the square root of two and the square root of (four plus three times the imaginary unit), then add three times the imaginary unit, and divide the entire quantity by two. One would expect the function to either simplify that nested radical or return it unchanged if it cannot be denested.

Runtime Error
Instead of producing a result, the function fails partway through its internal routine for splitting surds and raises an IndexError, indicating that it tried to access an element of a tuple that does not exist.

If an expression cannot be denested it should be returned unchanged.  
IndexError fixed for sqrtdenest.  
Fixes #12420  
Now if the expression can't be denested, it will be returned unchanged.

Old Result:
Attempting to denest the same expression repeatedly led to the identical failure mode: during the surd-splitting step, an internal tuple lookup went out of range and caused an IndexError.

New Result:

```
In [9]: sqrtdenest((3 - sqrt(2)*sqrt(4 + 3*I) + 3*I)/2)
Out[9]: 3/2 - sqrt(2)*sqrt(4 + 3*I)/2 + 3*I/2
```