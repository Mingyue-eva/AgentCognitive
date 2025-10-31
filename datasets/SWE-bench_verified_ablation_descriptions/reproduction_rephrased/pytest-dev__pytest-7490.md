## Issue Description
Pytest 6: Dynamically adding xfail marker in test no longer ignores failure

## Description

With pytest 5.x, we can dynamically add an xfail to a test `request` object using `request.node.add_marker(mark)` (see example below). In 5.x this treated the failing test like a test marked statically with an `xfail`. With 6.0.0rc0 it raises. 

## Versions

<details>

```
$ pip list
Package                       Version                         Location                                                      
----------------------------- ------------------------------- --------------------------------------------------------------
... (omitted for brevity) ...
pytest                        5.4.3                           
pytest-asyncio                0.10.0                          
pytest-cov                    2.8.1                           
pytest-forked                 1.0.2                           
pytest-repeat                 0.8.0                           
pytest-xdist                  1.29.0                          
... 
```

</details>

- pytest 5.4.3 on MacOS 10.14.5
- pytest 6.0.1rc0 on MacOS 10.14.5

In a file named `test_foo.py`, define a single test that takes the `request` fixture. Inside it, attach an `xfail` marker by calling `request.node.add_marker(pytest.mark.xfail(reason="xfail"))`, then immediately assert a false condition. When this file is run under pytest 5.4.3 with the `-rsx` flags, the test is reported as XFAIL. Running the same test under pytest 6.0.0rc0 with the same command instead produces a regular test failure.

With 5.4.3

```
$ pytest -rsx test_foo.py
=============================================================================== test session starts ================================================================================
platform darwin -- Python 3.7.6, pytest-5.4.3, py-1.9.0, pluggy-0.13.0
hypothesis profile 'default' -> database=DirectoryBasedExampleDatabase('/Users/taugspurger/sandbox/.hypothesis/examples')
rootdir: /Users/taugspurger/sandbox
plugins: xdist-1.29.0, hypothesis-4.36.2, forked-1.0.2, repeat-0.8.0, asyncio-0.10.0, cov-2.8.1
collected 1 item

test_foo.py x                                                                                                                                                                [100%]

============================================================================= short test summary info ==============================================================================
XFAIL test_foo.py::test_xfail_test
  xfail
================================================================================ 1 xfailed in 0.07s ================================================================================
```

With 6.0.0rc0

```
$ pytest -rsx test_foo.py
=============================================================================== test session starts ================================================================================
platform darwin -- Python 3.7.6, pytest-6.0.0rc1, py-1.9.0, pluggy-0.13.0
hypothesis profile 'default' -> database=DirectoryBasedExampleDatabase('/Users/taugspurger/sandbox/.hypothesis/examples')
rootdir: /Users/taugspurger/sandbox
plugins: xdist-1.29.0, hypothesis-4.36.2, forked-1.0.2, repeat-0.8.0, asyncio-0.10.0, cov-2.8.1
collected 1 item

test_foo.py F                                                                                                                                                                [100%]

===================================================================================== FAILURES =====================================================================================
_________________________________________________________________________________ test_xfail_test __________________________________________________________________________________

request = <FixtureRequest for <Function test_xfail_test>>

    def test_xfail_test(request):
        mark = pytest.mark.xfail(reason="xfail")
        request.node.add_marker(mark)
>       assert 0
E       assert 0

test_foo.py:7: AssertionError
```