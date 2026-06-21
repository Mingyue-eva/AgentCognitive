Regression in 5.2.3: pytest tries to collect random __init__.py files  
This was caught by our build server this morning. It seems that pytest 5.2.3 tries to import any `__init__.py` file under the current directory. (We have some package that is only used on windows and cannot be imported on linux.)

Here is a minimal example using tox that reproduces the problem (I'm running on Debian 10 with Python 3.7.3):

Reproduction steps and expected outcome  
First, create a directory named foobar and add an __init__.py file inside it containing a single assertion that always fails. Next, write a tox configuration that defines two environments: one using pytest 5.2.2 and the other using pytest 5.2.3, and instruct tox to skip building any distribution. Configure each environment to install its pinned pytest version and then invoke pytest. When you run tox, you expect both environments to install correctly and for pytest to collect only test files (such as a simple test_foo.py) and report one passing test in each case.

Observed behavior  
In the pytest 5.2.2 environment, pytest installs successfully, collects the one test in test_foo.py, and reports it as passed. In the pytest 5.2.3 environment, pytest again installs successfully but during collection it unexpectedly imports the foobar/__init__.py file. Because that file contains an assertion that always fails, pytest aborts immediately with an assertion error at collection time, and the test run is interrupted before any tests can be executed.