## Issue Description
Pytest 6: Dynamically adding xfail marker in test no longer ignores failure

With pytest 5.x, we can dynamically add an xfail to a test `request` object using `request.node.add_marker(mark)` (see example below). In 5.x this treated the failing test like a test marked statically with an `xfail`. With 6.0.0rc0 it raises.

## Versions

<details>

```
$ pip list
… (same as above) …
```

</details>

- [ ] pytest and operating system versions

Pytest 6.0.1rc0 and MacOS 10.14.5

```python
# file: test_foo.py
import pytest

def test_xfail_test(request):
    mark = pytest.mark.xfail(reason="xfail")
    request.node.add_marker(mark)
    assert 0
```

With 5.4.3

```
$ pytest -rsx test_foo.py
… 
test_foo.py x                                                                                                                                                                [100%]
… 1 xfailed in 0.07s …
```

With 6.0.0rc0

When pytest 6.0.0rc1 runs the same test, it still collects and executes it, but instead of treating the failed assertion as an expected xfail, it flags it as a hard failure. The `assert 0` raises an AssertionError, and pytest reports the test as failed (marked ‘F’) rather than xfailed.