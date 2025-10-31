[Bug]: DPI of a figure is doubled after unpickling on M1 Mac  
### Bug summary  

When a figure is unpickled, its dpi is doubled. This behaviour happens every time and if done in a loop it can cause an `OverflowError`.  

### Code for reproduction  

First, import NumPy, Matplotlib (including pyplot), pickle, and the platform module, and print out the current Matplotlib backend, version information, operating system details, and Python version. Then create a new Matplotlib figure and plot a sine curve. To reproduce the issue, run a loop in which you serialize the figure to a file using pickle, immediately read it back, and after each reload print the figure’s current dpi.  

### Actual outcome  

When running the above procedure on an M1 Mac with Matplotlib 3.5.2 and Python 3.9.12, the sequence of dpi values doubles on every reload, for example:  
0: 200.0  
1: 400.0  
2: 800.0  
…  
21: 419430400.0  

After around the twenty‐second reload, the dpi value grows so large that attempting to restore the figure again triggers an overflow error. The process terminates with an error indicating that a signed integer exceeded the maximum allowed value.  

### Expected outcome  

```
MacOSX
Matplotlib ver: 3.5.2
Platform: macOS-12.4-arm64-arm-64bit
System: Darwin
Release: 21.5.0
Python ver: 3.9.12
0: 200.0
1: 200.0
2: 200.0
3: 200.0
4: 200.0
5: 200.0
6: 200.0
7: 200.0
8: 200.0
9: 200.0
10: 200.0
11: 200.0
12: 200.0
13: 200.0
14: 200.0
15: 200.0
16: 200.0
17: 200.0
18: 200.0
19: 200.0
20: 200.0
21: 200.0
22: 200.0
```

### Additional information  

This seems to happen only on M1 MacBooks and the version of python doesn't matter.  

### Operating system  

OS/X  

### Matplotlib Version  

3.5.2  

### Matplotlib Backend  

MacOSX  

### Python version  

3.9.12  

### Jupyter version  

_No response_  

### Installation  

pip