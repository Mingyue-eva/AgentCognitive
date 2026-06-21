## Issue Description
[Bug]: NumPy 1.24 deprecation warnings

### Bug summary
Starting NumPy 1.24 I observe several deprecation warnings.

### Code for reproduction
```python
import matplotlib.pyplot as plt
import numpy as np

plt.get_cmap()(np.empty((0, ), dtype=np.uint8))
```

### Actual outcome
Matplotlib emits deprecation warnings indicating that in future releases NumPy will no longer permit converting out-of-range Python integers (for example 256, 257 or 258) into uint8 arrays. Currently these values wrap around, but that behavior will be removed. The warnings suggest using `np.array(value).astype(dtype)` if the overflow‐wrapped result is desired.

### Expected outcome
No warnings.

### Additional information
_No response_

### Operating system
ArchLinux

### Matplotlib Version
3.6.2

### Matplotlib Backend
QtAgg

### Python version
Python 3.10.9

### Jupyter version
_No response_

### Installation
Linux package manager