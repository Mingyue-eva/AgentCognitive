[Bug]: Confusing deprecation warning when empty data passed to axis with category units

### Bug summary

I'm seeing a MatplotlibDeprecationWarning when calling axes methods on empty data structures for axes that are using string unit converters. I think this is either a false alarm or a non-actionable warning.

### Code for reproduction

To reproduce the issue, start by creating a new figure and obtaining its axis object. Next, configure the x-axis to use categorical units by supplying two category labels, “a” and “b.” Finally, invoke the plotting function while providing empty sequences for both x and y values.

### Actual outcome

When the plot call is executed, Matplotlib emits a deprecation warning indicating that passing numeric values through unit converters has been deprecated since version 3.5 and will be removed in a future release, and it suggests using the axis’s `convert_units` method instead. If warnings are treated as errors, the process terminates with a ConversionError stating that it failed to convert the empty array into axis units.

Additionally, when attempting to follow the warning’s own advice by calling the axis’s `convert_xunits` method directly with an empty list, the same deprecation warning is issued and the same ConversionError is raised, again complaining that the empty input cannot be converted to axis units.

### Expected outcome

I would expect this to either (1) continue producing artists with no data, or (2) more accurately describe what the problem is and how to avoid it.

### Additional information

Looking at the traceback, it seems like it's catching exceptions too broadly and issuing a generic warning. If passing empty data structures through unit converters is now deprecated, it should be possible to detect that specific case.

But I can't quite follow the API change note here:

> Previously, custom subclasses of [units.ConversionInterface](https://matplotlib.org/devdocs/api/units_api.html#matplotlib.units.ConversionInterface) needed to implement a convert method that not only accepted instances of the unit, but also unitless values (which are passed through as is). This is no longer the case (convert is never called with a unitless value) ... Consider calling [Axis.convert_units](https://matplotlib.org/devdocs/api/_as_gen/matplotlib.axis.Axis.convert_units.html#matplotlib.axis.Axis.convert_units) instead, which still supports unitless values.

The traceback appears inconsistent with the claim that `convert` is never called with a unit-less value and that `convert_units` provides an alternate, supported interface.

### Matplotlib Version

3.5.1