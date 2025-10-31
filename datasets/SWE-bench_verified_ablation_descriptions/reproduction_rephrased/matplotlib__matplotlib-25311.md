[Bug]: Unable to pickle figure with draggable legend

### Bug summary

I am unable to pickle figure with draggable legend. Same error comes for draggable annotations.

### Code for reproduction

I created a Matplotlib figure and added a single subplot. I defined time points [0, 1, 2, 3, 4] and corresponding speed values [40, 43, 45, 47, 48], plotted them with the label “speed,” then enabled dragging on the legend. Once the legend was set to be draggable, I attempted to serialize the entire figure by calling `pickle.dumps(fig)`.

### Actual outcome

TypeError: cannot pickle 'FigureCanvasQTAgg' object

### Expected outcome

The figure should be pickled successfully without raising any errors.

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