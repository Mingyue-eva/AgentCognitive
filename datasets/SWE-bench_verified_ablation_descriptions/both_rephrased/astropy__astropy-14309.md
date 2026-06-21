## Description
Cron tests in HENDRICS using `identify_format` have started failing in the `devdeps` environment. When the code tries to detect the file format for writing a table, the FITS connector looks for an HDU object in the positional arguments but none is provided. As a result, it attempts to access the first element of an empty tuple and raises an IndexError about a tuple index being out of range.

As per a Slack conversation with @saimn and @pllim, this should be related to https://github.com/astropy/astropy/commit/2a0c5c6f5b982a76615c544854cd6e7d35c67c7f

Citing @saimn: When `filepath` is a string without a FITS extension, the function was returning None, now it executes `isinstance(args[0], ...)`

### Steps to Reproduce
Start a Python session and import the format registry and table classes. Then ask the registry which formats can be used to write a Table to a file named “bububu.ecsv.” Since the extension is `.ecsv`, you would expect it to recognize the ECSV format and return it. Instead, the call fails with an IndexError because the FITS identifier tries to examine a non-existent positional argument.

### System Details
<!-- Even if you do not think this is necessary, it is useful information for the maintainers.
Please run the following snippet and paste the output below:
import platform; print(platform.platform())
import sys; print("Python", sys.version)
import numpy; print("Numpy", numpy.__version__)
import erfa; print("pyerfa", erfa.__version__)
import astropy; print("astropy", astropy.__version__)
import scipy; print("Scipy", scipy.__version__)
import matplotlib; print("Matplotlib", matplotlib.__version__)
-->