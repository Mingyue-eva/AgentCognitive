Pytest 6: Dynamically adding xfail marker in test no longer ignores failure

Description

With pytest 5.x, we could dynamically add an xfail marker to a test using `request.node.add_marker(mark)` and have failures treated as expected xfails. In pytest 6.0.0rc0 and later, dynamically added xfail markers no longer prevent a failing test from being reported as a failure.

Versions

pytest 6.0.1rc0 on macOS 10.14.5