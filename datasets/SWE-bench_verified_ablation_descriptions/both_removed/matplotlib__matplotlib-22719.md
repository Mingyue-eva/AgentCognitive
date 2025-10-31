[Bug]: Confusing deprecation warning when empty data passed to axis with category units

### Bug summary

I'm seeing a MatplotlibDeprecationWarning when calling axes methods on empty data structures for axes that are using string unit converters. I think this is either a false alarm or a non-actionable warning.

### Expected outcome

I would expect this to either (1) continue producing artists with no data, or (2) more accurately describe what the problem is and how to avoid it.

### Additional information

Looking at the implementation, it seems exceptions are caught too broadly and a generic warning is issued. The change note indicates that custom `convert` methods no longer receive unit-less values and that `Axis.convert_units` should be used instead, yet the warning still appears for empty data, suggesting this edge case wasn't anticipated.

### Matplotlib Version

3.5.1