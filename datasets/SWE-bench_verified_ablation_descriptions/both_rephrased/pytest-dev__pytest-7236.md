unittest.TestCase.tearDown executed on skipped tests when running --pdb

With this minimal test:
A TestCase subclass defines a setUp method that runs some placeholder code, a test method that is explicitly skipped, and a tearDown method that also runs placeholder code. The goal is simply to observe whether tearDown is invoked when the test is skipped.

```
$ python --version
Python 3.6.10
$ pip freeze
attrs==19.3.0
importlib-metadata==1.6.0
more-itertools==8.2.0
packaging==20.3
pluggy==0.13.1
py==1.8.1
pyparsing==2.4.7
six==1.14.0
wcwidth==0.1.9
zipp==3.1.0
```

test is properly skipped:
When running pytest normally on this file, the framework discovers the single test, recognizes the skip decorator, and reports one skipped test. No teardown code is executed and the session ends cleanly with only a skip message.

but when running with `--pdb`, the teardown seems executed:
Starting pytest with the option to drop into the debugger on errors causes the skipped test’s tearDown method to still run. Because that teardown refers to undefined placeholder logic, a name lookup failure occurs at teardown time, triggering the debugger entry. The final test summary then shows one skipped test and one error rather than just the skip.

I would have expected the test to be skipped, even with `--pdb`. With `pytest==5.4.1`, test was also skipped with `--pdb`, so this seems to be a change between 5.4.2 and 5.4.1.

(I would have loved to, but I don't have time to send a PR these days)