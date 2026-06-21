[Bug]: NumPy 1.24 deprecation warnings

### Bug summary

Starting NumPy 1.24 I observe several deprecation warnings.

### Code for reproduction

In a Python environment, import Matplotlib’s pyplot module and NumPy. Then create an empty array of 8-bit unsigned integers and pass it to the default colormap obtained via pyplot’s get_cmap. This sequence triggers the warnings.

### Actual outcome

When the colormap is applied to the empty uint8 array, three deprecation warnings are emitted from Matplotlib’s color handling code. Each warning notes that future versions of NumPy will no longer allow conversion of out-of-bound Python integers into unsigned 8-bit integer arrays, pointing out values just above, below, and within the limit that currently overflow silently but will be disallowed later.

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