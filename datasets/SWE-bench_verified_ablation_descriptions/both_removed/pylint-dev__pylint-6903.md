Running pylint in Kubernetes Pod with --jobs=0 fails

### Bug description

I run pylint in multiple parallel stages with Jenkins at a Kubernetes agent with `--jobs=0`. The newly introduced function pylint.run._query_cpu() is called to determine the number of CPUs to use and returns 0 in this case. This leads to a crash of pylint because the multiprocessing pool requires a value greater than 0. The calculation in the function is cast to an integer and thus yields 0.

### Configuration

_No response_

### Expected behavior

I expect pylint to not crash if the number of available CPUs is miscalculated in this special case. The calculated number should never be 0. A possible solution would be to append an `or 1` at the end of the calculation.

### Pylint version

pylint>2.14.0

### OS / Environment

Ubuntu 20.04  
Kubernetes Version: v1.18.6  
Python 3.9.12

### Additional dependencies

_No response_