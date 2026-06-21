BytesWarning when using --setup-show with bytes parameter

With Python 3.8.2, pytest 5.4.1 (or latest master; stacktraces are from there) and this file:

```python
import pytest

@pytest.mark.parametrize('data', [b'Hello World'])
def test_data(data):
    pass
```

when running `python3 -bb -m pytest --setup-show`, pytest fails during the setup of `test_data[Hello World]` because its fixture reporting code tries to convert the bytes parameter to a string. That implicit `str()` call on a bytes object raises a `BytesWarning` at `src/_pytest/setuponly.py:69`.

Shouldn't that be using `saferepr` or something rather than (implicitly) `str()`?