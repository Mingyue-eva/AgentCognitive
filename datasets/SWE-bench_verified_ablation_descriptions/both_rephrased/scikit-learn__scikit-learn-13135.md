KBinsDiscretizer: kmeans fails due to unsorted bin_edges

#### Description
`KBinsDiscretizer` with `strategy='kmeans` fails in certain situations, due to centers and consequently bin_edges being unsorted, which is fatal for np.digitize. 

#### Steps to Reproduce
Create a one-dimensional dataset with the values 0, 0.5, 2, 3, 9, and 10. Configure a KBinsDiscretizer to use five bins, the kmeans strategy, and ordinal encoding. Fit this discretizer to the dataset and then apply the transformation. (A similar failure can occur in production when selecting a reasonable number of bins, for example on the order of the logarithm of the number of unique input values.)

#### Expected Results
The discretizer should fit the data and perform the transformation without raising any exceptions.

#### Actual Results
When transforming the data, a runtime error is raised because the bin edges produced by kmeans are not sorted, and the digitization routine rejects unsorted boundaries.

#### Versions
System:
   machine: Linux-4.15.0-45-generic-x86_64-with-Ubuntu-16.04-xenial
    python: 3.5.2 (default, Nov 23 2017, 16:37:01)  [GCC 5.4.0 20160609]
executable: /home/sandro/.virtualenvs/scikit-learn/bin/python

BLAS:
  lib_dirs: 
    macros: 
cblas_libs: cblas

Python deps:
     scipy: 1.1.0
setuptools: 39.1.0
     numpy: 1.15.2
   sklearn: 0.21.dev0
    pandas: 0.23.4
    Cython: 0.28.5
       pip: 10.0.1