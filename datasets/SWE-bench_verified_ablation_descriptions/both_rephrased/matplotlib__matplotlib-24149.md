[Bug]: ax.bar raises for all-nan data on matplotlib 3.6.1 

### Bug summary

`ax.bar` raises an exception in 3.6.1 when passed only nan data. This irrevocably breaks seaborn's histogram function (which draws and then removes a "phantom" bar to trip the color cycle).

### Code for reproduction

To reproduce this issue, start a Python session, import NumPy and Matplotlib’s plotting module, create a new figure and axes, and then attempt to draw a bar chart by passing a single x-position and a single height value that are both NaN.

### Actual outcome

Instead of returning a bar chart object, the method fails during input validation. It looks for a finite value in the provided sequences, finds none, and raises a StopIteration error. No bars are drawn and the call terminates with an exception.

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