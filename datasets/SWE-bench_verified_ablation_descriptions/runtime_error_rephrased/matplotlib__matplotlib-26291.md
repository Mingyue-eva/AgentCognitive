## Issue Description
[Bug]: Error while creating inset axes using `mpl_toolkits.axes_grid1.inset_locator.inset_axes`

### Bug summary
Unable to create the inset axes in a plot using the code (following the first example on the website as posted here).

### Code for reproduction
```python
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1.inset_locator import inset_axes

fig, (ax, ax2) = plt.subplots(1, 2, figsize=[5.5, 2.8])
axins = inset_axes(ax, width=1.3, height=0.9)
plt.show()
```

### Actual outcome
When the figure is rendered, Matplotlib raises an AttributeError stating that a `'NoneType' object has no attribute '_get_renderer'`. According to the traceback, during the tight bounding‐box adjustment the inset locator calls `get_window_extent` on an `OffsetBox`, which in turn invokes `figure._get_renderer()`. Because the figure’s renderer hasn’t been initialized (the figure object is effectively `None` in that context), the attempt to access `_get_renderer` fails.

### Expected outcome
I was expecting to add an empty box towards the top right of the first subplot (with axes `ax`) in the figure, as shown in the demo on the website.

### Additional information
_No response_

### Operating system
Arch linux: 6.4.2-arch1-1

### Matplotlib Version
3.7.2

### Matplotlib Backend
module://matplotlib_inline.backend_inline

### Python version
Python 3.8.17

### Jupyter version
Jupyter lab: 3.6.5

### Installation
conda