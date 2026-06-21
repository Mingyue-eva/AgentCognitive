[Bug]: Unable to pickle figure with aligned labels

### Bug summary

Unable to pickle figure after calling `align_labels()`

### Code for reproduction

In a Python session with Matplotlib, create a new figure and add two subplots stacked vertically. On the first subplot, plot a series of speed values against time and label the y-axis “speed.” On the second subplot, plot a series of acceleration values against the same time points and label that y-axis “acc.” After plotting, call the function that aligns all y-axis labels across subplots. Then attempt to serialize the entire figure object using Python’s pickle mechanism and finally display the figure.

### Actual outcome

When the pickling function is invoked immediately after aligning the labels, a type error occurs indicating that an internal reference type used by the alignment routine cannot be serialized.

### Expected outcome

Pickling successful

### Additional information

_No response_

### Operating system

Windows

### Matplotlib Version

3.7.0

### Matplotlib Backend

_No response_

### Python version

_No response_

### Jupyter version

_No response_

### Installation

None