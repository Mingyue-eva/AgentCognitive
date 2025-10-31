## Issue Description
Cron tests in HENDRICS using identify_format have started failing in `devdeps` (e.g. here) with an IndexError caused by the FITS identifier attempting to access the first element of its positional‐arguments tuple even though that tuple is empty.

As per a Slack conversation with @saimn and @pllim, this should be related to https://github.com/astropy/astropy/commit/2a0c5c6f5b982a76615c544854cd6e7d35c67c7f  
Citing @saimn: When `filepath` is a string without a FITS extension, the function was returning None; now it falls through to execute `isinstance(args[0], ...)`, which fails when `args` is empty.

### Steps to Reproduce
```python
In [1]: from astropy.io.registry import identify_format
In [2]: from astropy.table import Table

In [3]: identify_format("write", Table, "bububu.ecsv", None, [], {})
```
This call raises an IndexError because the FITS format checker tries to inspect its first positional argument for FITS validation even though no positional arguments were provided.

### System Details
<!-- Even if you do not think this is necessary, it is useful information for the maintainers.
Please run the following snippet and paste the output below:
import platform; print(platform.platform())
import sys; print("Python", sys.version)
import numpy; print("Numpy", numpy.__version__)
import erfa; print("pyerfa", erfa.__version__)
import astropy; print("astropy", astropy.__version__)
import scipy; print("Scipy", scipy.__version__)
import matplotlib; print("Matplotlib", matplotlib.__version__) -->
