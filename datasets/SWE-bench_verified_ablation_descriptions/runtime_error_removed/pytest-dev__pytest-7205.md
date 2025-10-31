## Issue Description
BytesWarning when using --setup-show with bytes parameter

With Python 3.8.2, pytest 5.4.1 (or latest master) and this file:

```python
import pytest

@pytest.mark.parametrize('data', [b'Hello World'])
def test_data(data):
    pass
```

When running `python3 -bb -m pytest --setup-show`, an error occurs during fixture setup.

Shouldn't that be using `saferepr` or something rather than (implicitly) `str()`?