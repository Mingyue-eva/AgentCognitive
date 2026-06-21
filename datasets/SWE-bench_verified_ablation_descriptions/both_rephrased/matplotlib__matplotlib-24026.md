stackplot should not change Axes cycler  
Usecase: I am producing various types of plots (some use rectangle collections, some regular plot-lines, some stacked plots) and wish to keep the colors synchronized across plot types for consistency and ease of comparison.

Reproduction:
A small numeric dataset with three series is prepared. A figure and axes are created. On that axes, a line segment is drawn using the first color in the default cycle. A rectangular patch is then added at a specified position using the second color in the cycle. After that, a stacked area plot is requested with the same x-axis values and the three data series, explicitly asking for the third, fourth, and fifth colors by their cycle aliases. The expected behavior is that the stackplot draws its layers in those specified colors and leaves the axes’ color cycle intact so further plots will continue using the next colors in sequence.

Error:
When the stackplot function receives these cycle-alias color references, it attempts to set the axes’ property cycle to that list. During that operation, the color validator rejects alias references as invalid inputs for a property cycler, causing the call to fail with a ValueError stating that a cycle reference cannot be used in the cycler.

_Originally posted by @hmedina in https://github.com/matplotlib/matplotlib/issues/14221#issuecomment-1259779507_