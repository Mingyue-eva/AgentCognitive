Regression in 5.2.3: pytest tries to collect random __init__.py files  
This was caught by our build server this morning. It seems that pytest 5.2.3 tries to import any `__init__.py` file under the current directory. (We have some package that is only used on windows and cannot be imported on linux.)  

Here is a minimal example using tox that reproduces the problem (I'm running on Debian 10 with Python 3.7.3):  
❯❯❯ mkdir foobar  
❯❯❯ echo 'assert False' >! foobar/__init__.py  
❯❯❯ cat > tox.ini <<EOF  
[tox]  
envlist = py37-pytest{522,523}  
skipsdist = true  

[testenv]  
deps =  
    pytest522: pytest==5.2.2  
    pytest523: pytest==5.2.3  
commands = pytest  
EOF  
❯❯❯ tox  

When running under pytest 5.2.3, pytest attempted to import and execute foobar/__init__.py during test collection. Since that file contains an unconditional assert False, pytest raised an AssertionError while collecting tests, aborted the session, and tox reported the pytest command failure with exit code 2.