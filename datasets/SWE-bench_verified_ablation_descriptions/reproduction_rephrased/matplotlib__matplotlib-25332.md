[Bug]: Unable to pickle figure with aligned labels  
### Bug summary  
Unable to pickle figure after calling `align_labels()`  

### Reproduction steps  
Create a Matplotlib figure and add two subplots stacked vertically. Define a time array `[0, 1, 2, 3, 4]`, a speed array `[40000, 4300, 4500, 4700, 4800]`, and an acceleration array `[10, 11, 12, 13, 14]`. On the first subplot, plot time versus speed and set the y-axis label to “speed”. On the second subplot, plot time versus acceleration and set its y-axis label to “acc”. After calling `fig.align_labels()` to align those labels, attempt to serialize the figure with `pickle.dumps(fig)`.

### Actual outcome  
```
align.py", line 16
    pickle.dumps(fig)
TypeError: cannot pickle 'weakref.ReferenceType' object
```

### Expected outcome  
The figure should be pickled successfully without errors.

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