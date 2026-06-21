docutils reports an error rendering view docstring when the first line is not empty  
Description  
  
Currently admindoc works correctly only with docstrings where the first line is empty, and all Django docstrings are formatted in this way. However, if the docstring text begins immediately on the first line after the opening triple quotes, you can reproduce the failure by defining such a function and then viewing its documentation in the Django admin. You would expect the docstring to appear normally, but instead the rendering process stops.  
  
When you run the documentation build, docutils fails while processing the default-role directive and reports that no content is permitted at that point, so the view docstring is not displayed.  
  
The culprit is this code in trim_docstring:  
indent = min(len(line) - len(line.lstrip()) for line in lines if line.lstrip())  
The problem is that the indentation of the first line is 0.  
The solution is to skip the first line:  
indent = min(len(line) - len(line.lstrip()) for line in lines[1:] if line.lstrip())  
Thanks.