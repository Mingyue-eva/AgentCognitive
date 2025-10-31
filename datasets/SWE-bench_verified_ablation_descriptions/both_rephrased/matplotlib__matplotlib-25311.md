[Bug]: Unable to pickle figure with draggable legend

### Bug summary

I am unable to pickle figure with draggable legend. Same error comes for draggable annotations.

### Reproduction steps and expected outcome

On Windows 10 with Python 3.10 and Matplotlib 3.7.0 installed via pip, open a new figure and add a single subplot. Plot a series of time versus speed values, add a legend to the plot, and enable the legend’s draggable feature. Then attempt to serialize the entire figure using the pickle module. The expected outcome is that pickle.dumps completes without error and the figure object is successfully serialized.

### Actual outcome

When serialization is attempted on a figure that contains a draggable legend, a TypeError is raised indicating that a FigureCanvasQTAgg object cannot be pickled.

### Additional information

_No response_

### Operating system

Windows 10

### Matplotlib Version

3.7.0

### Matplotlib Backend

_No response_

### Python version

3.10

### Jupyter version

_No response_

### Installation

pip