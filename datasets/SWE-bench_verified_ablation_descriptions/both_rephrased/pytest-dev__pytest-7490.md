Pytest 6: Dynamically adding xfail marker in test no longer ignores failure

## Description

With pytest 5.x, we can dynamically add an xfail to a test `request` object using `request.node.add_marker(mark)` (see example below). In 5.x this treated the failing test like a a test marked statically with an `xfail`. With 6.0.0rc0 it raises. 

## Versions

<details>

```
$ pip list
Package                       Version                         Location                                                      
----------------------------- ------------------------------- --------------------------------------------------------------
a                             1.0                             
aioftp                        0.13.0                          
aiohttp                       3.6.2                           
… (other packages omitted for brevity) …
zope.interface                4.7.1                           
```

</details>

- [ ] pytest and operating system versions

Pytest 6.0.1rc0 and MacOS 10.14.5

To reproduce the issue, create a test file that defines a single test function. In that function, obtain the built-in request fixture, apply an xfail marker dynamically to the current test node, and then perform an assertion that is guaranteed to fail. When running pytest version 5.4.3 with the “-rsx” option on macOS, the test suite reports that this test was expected to fail: the failure is suppressed and the summary shows one xfailed test. Under pytest version 6.0.0rc1 in the same environment, running the identical test causes the assertion to be reported as an ordinary failure despite the dynamic xfail marker. The test runner indicates a failure rather than an xfail, and the summary reflects one failed test instead of one xfailed.