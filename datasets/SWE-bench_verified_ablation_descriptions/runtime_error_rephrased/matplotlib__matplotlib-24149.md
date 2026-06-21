## Issue Description
[Bug]: ax.bar raises for all-nan data on matplotlib 3.6.1  
### Bug summary

`ax.bar` raises an exception in 3.6.1 when passed only nan data. This irrevocably breaks seaborn's histogram function (which draws and then removes a "phantom" bar to trip the color cycle).

### Code for reproduction

```python
import numpy as np
import matplotlib.pyplot as plt
f, ax = plt.subplots()
ax.bar([np.nan], [np.nan])
```

### Actual outcome

When `ax.bar` is called with only NaN values, Matplotlib attempts to find a finite x coordinate but cannot, causing a StopIteration exception in the helper function that looks for the first finite element.

### Expected outcome

On 3.6.0 this returns a `BarCollection` with one Rectangle, having `nan` for `x` and `height`.

### Additional information

I assume it's related to this bullet in the release notes:

- Fix barplot being empty when first element is NaN

But I don't know the context for it to investigate further (could these link to PRs?)

Further debugging:

```python
ax.bar([np.nan], [0])  # Raises
ax.bar([0], [np.nan])  # Works
```

So it's about the x position specifically.

### Operating system

Macos

### Matplotlib Version

3.6.1

### Matplotlib Backend

_No response_

### Python version

_No response_

### Jupyter version

_No response_

### Installation

pip