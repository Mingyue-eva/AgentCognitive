Regression in 5.2.3: pytest tries to collect random __init__.py files  
This was caught by our build server this morning. It seems that pytest 5.2.3 tries to import any `__init__.py` file under the current directory. (We have some package that is only used on windows and cannot be imported on linux.)

To reproduce on Debian 10 with Python 3.7.3, create a directory named foobar and put an `__init__.py` inside that simply does `assert False`. Then use a `tox.ini` that defines two environments—one pinned to pytest 5.2.2, the other to pytest 5.2.3—and have both run `pytest`. When you run `tox`, the pytest 5.2.2 environment executes the tests and reports success, but the pytest 5.2.3 environment unexpectedly tries to import `foobar/__init__.py` and triggers the assertion, producing this error:

==================================== ERRORS ====================================  
_____________________ ERROR collecting foobar/__init__.py ______________________  
foobar/__init__.py:1: in <module>  
    assert False  
E   AssertionError  
!!!!!!!!!!!!!!!!!!! Interrupted: 1 errors during collection !!!!!!!!!!!!!!!!!!!!  
=============================== 1 error in 0.04s ===============================  
ERROR: InvocationError for command '/tmp/gregoire/tmp.Fm6yiwvARV/.tox/py37-pytest523/bin/pytest' (exited with code 2)  
___________________________________ summary ____________________________________  
  py37-pytest522: commands succeeded  
ERROR:   py37-pytest523: commands failed