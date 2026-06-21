[Bug]: Confusing deprecation warning when empty data passed to axis with category units  
### Bug summary  
I’m seeing a MatplotlibDeprecationWarning when calling axes methods on empty data structures for axes that are using string unit converters. I think this is either a false alarm or a non-actionable warning.  

### Code for reproduction  
```python
import matplotlib.pyplot as plt
f, ax = plt.subplots()
ax.xaxis.update_units(["a", "b"])
ax.plot([], [])
```  

### Actual outcome  
When `ax.plot([], [])` is executed, Matplotlib issues a deprecation warning because it detects an empty numerical array being run through the category unit converter. The warning reads that passing numbers through unit converters is deprecated since version 3.5 and will be removed in a future release, and suggests using `Axis.convert_units` instead. In environments where warnings are turned into errors, this deprecation notice is raised as a `MatplotlibDeprecationWarning` and then wrapped in a `ConversionError`, reporting that it failed to convert the empty array to axis units.  

When attempting to follow the advice by calling `ax.convert_xunits([])`, the same deprecation warning is emitted and again escalates to a `ConversionError`, this time stating that it could not convert the empty list to axis units.  

### Expected outcome  
I would expect this to either (1) continue producing artists with no data, or (2) more accurately describe what the problem is and how to avoid it.  

### Additional information  
Looking at the traceback, it seems like it’s catching exceptions too broadly and issuing a generic warning. If passing empty data structures through unit converters is now deprecated, it should be possible to detect that specific case.  

But I can’t quite follow the API change note here:

> Previously, custom subclasses of units.ConversionInterface needed to implement a convert method that not only accepted instances of the unit, but also unitless values (which are passed through as is). This is no longer the case (convert is never called with a unit-less value) … Consider calling Axis.convert_units instead, which still supports unitless values.

The traceback appears inconsistent with the claim that `convert` is never called with a unit-less value and that `convert_units` provides an alternate, supported interface. So it feels like whatever is changing behind the scenes failed to anticipate the “empty data” edge case.  

### Matplotlib Version  
3.5.1