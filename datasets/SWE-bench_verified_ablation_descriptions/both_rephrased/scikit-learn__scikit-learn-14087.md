IndexError thrown with LogisticRegressionCV and refit=False

#### Description
The following error is thrown when trying to estimate a regularization parameter via cross-validation, *without* refitting.

#### Steps to Reproduce
Generate a dataset by drawing 1,000 samples of three features from a normal distribution, then create binary targets by applying a random linear model with an intercept and taking the sign of the result. Configure a logistic regression cross-validation estimator with five folds, use either the ‘saga’ or ‘liblinear’ solver, set the tolerance to 1e-2, and disable refitting. Fitting this estimator on the generated data triggers the issue.

#### Expected Results
The cross-validation procedure completes without any errors and returns the selected regularization parameters.

#### Actual Results
When fitting the model under these settings, the process fails with an indexing error. During the averaging of coefficient paths across folds, the implementation attempts to access an array with an invalid number of dimensions, causing the fit method to abort with an exception.

#### Versions
```
System:
    python: 3.6.7 (default, May 13 2019, 16:14:45)  [GCC 4.2.1 Compatible Apple LLVM 10.0.1 (clang-1001.0.46.4)]
executable: /Users/tsweetser/.pyenv/versions/3.6.7/envs/jupyter/bin/python
   machine: Darwin-18.6.0-x86_64-i386-64bit

BLAS:
    macros: NO_ATLAS_INFO=3, HAVE_CBLAS=None
  lib_dirs: 
cblas_libs: cblas

Python deps:
       pip: 19.1.1
setuptools: 39.0.1
   sklearn: 0.21.2
     numpy: 1.15.1
     scipy: 1.1.0
    Cython: 0.29.6
    pandas: 0.24.2
```