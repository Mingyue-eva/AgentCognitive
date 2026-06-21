[Bug]: get_backend() clears figures from Gcf.figs if they were created under rc_context

### Bug summary

calling `matplotlib.get_backend()` removes all figures from `Gcf` if the *first* figure in `Gcf.figs` was created in an `rc_context`.

### Reproduction steps

1. Start a Python session and import `matplotlib.pyplot` and the `rc_context` utility.
2. Enter an `rc_context` block so that any default plotting settings are temporarily applied.
3. Within that block, create a new Matplotlib figure.
4. Immediately after leaving the block, record the internal registry of active figures (`Gcf.figs`) along with the identifier of the registry object.
5. Call `matplotlib.get_backend()` to retrieve the current backend.
6. Record the registry of active figures again in the same way.
7. Compare the two recordings. When the first figure was created inside the `rc_context`, you will see that the registry is cleared by the call to `get_backend()`.

### Actual outcome

When you compare the registry before and after invoking `get_backend()`, the initial snapshot shows a single figure manager entry, but the subsequent snapshot shows an empty registry. This mismatch causes an assertion failure, indicating that the figure has unexpectedly disappeared from `Gcf` after calling `get_backend()`.

### Expected outcome

The figure should not be missing from `Gcf`.  Consequences of this are, e.g, `plt.close(fig2)` doesn't work because `Gcf.destroy_fig()` can't find it.

### Additional information

_No response_

### Operating system

Xubuntu

### Matplotlib Version

3.5.2

### Matplotlib Backend

QtAgg

### Python version

Python 3.10.4

### Jupyter version

n/a

### Installation

conda