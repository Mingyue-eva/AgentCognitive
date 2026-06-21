exception serialization should include chained exceptions

To reproduce the issue, create two test functions that each raise a sequence of ValueError exceptions. In the first function, you throw an initial ValueError, catch it, then raise a second ValueError explicitly chained to the first, catch that, and finally raise a third ValueError chained to the second. In the second function, you throw a first ValueError, catch it, re-raise a second ValueError without using explicit chaining, catch that, and then raise a third ValueError.

When you run these tests with pytest in the normal mode, you see a detailed report of every exception in the chain. The test output first shows the original ValueError, then explains that it was the cause of the next ValueError, and finally that the second was the cause of the third. In the version without explicit chaining, pytest notes that one exception occurred during the handling of the previous one, and again when moving to the next, before showing the final error.

When you run the same tests under pytest-xdist with parallel workers, the output is truncated to show only the last exception in each test. Instead of the full chain, you only see the final ValueError reported for each function.

my setup:
```
pytest           4.0.2       
pytest-xdist     1.25.0
```