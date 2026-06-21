## Issue Description
[Bug]: Confusing deprecation warning when empty data passed to axis with category units

### Bug summary
I'm seeing a MatplotlibDeprecationWarning when calling axes methods on empty data structures for axes that are using string unit converters. I think this is either a false alarm or a non-actionable warning.

### Code for reproduction
```python
import matplotlib.pyplot as plt
f, ax = plt.subplots()
ax.xaxis.update_units(["a", "b"])
ax.plot([], [])
```

### Actual outcome
A MatplotlibDeprecationWarning is issued when calling `ax.plot([], [])`.

### Expected outcome
I would expect this to either (1) continue producing artists with no data, or (2) more accurately describe what the problem is and how to avoid it.

### Additional information
Looking at the behavior, it seems like the code is catching exceptions too broadly and issuing a generic warning. If passing empty data structures through unit converters is now deprecated, it should be possible to detect that specific case.

The API notes mention that custom subclasses of `units.ConversionInterface` previously had to accept unitless values in `convert`, but now `convert` is never called with unitless values and `Axis.convert_units` should be used instead. However, the empty-data edge case does not appear to be handled differently by `Axis.convert_units`.

Matplotlib Version: 3.5.1