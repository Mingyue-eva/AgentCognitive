GaussianMixture predict and fit_predict disagree when n_init>1

#### Description
When `n_init` is specified in GaussianMixture, the results of fit_predict(X) and predict(X) are often different.  The `test_gaussian_mixture_fit_predict` unit test doesn't catch this because it does not set `n_init`.

#### Steps/Code to Reproduce
Generate a dataset of one thousand samples with five features each drawn from a standard normal distribution. First, create a GaussianMixture model with five components and use it to both fit the model and predict cluster labels on the data. Verify that the labels returned by the combined fit_predict call exactly match those returned by calling predict on the fitted model. Next, repeat the same process but this time initialize the model with five random restarts (`n_init=5`), fit it again, and compare the two sets of labels in the same way.

#### Expected Results
In both the default case and when using five initializations, the cluster labels obtained from fit_predict should be identical to those obtained by fitting the model and then calling predict. No assertion errors or other exceptions should occur.

#### Actual Results
When the model is run with five random initializations, the labels from fit_predict and predict differ substantially (approximately 88.6% of the labels do not match), causing the comparison check to fail with an assertion indicating that the two arrays of cluster assignments are not equal.

#### Versions
```
System:
    python: 2.7.15rc1 (default, Nov 12 2018, 14:31:15)  [GCC 7.3.0]
   machine: Linux-4.15.0-43-generic-x86_64-with-Ubuntu-18.04-bionic
executable: /usr/bin/python

BLAS:
    macros: HAVE_CBLAS=None, NO_ATLAS_INFO=-1
cblas_libs: cblas
  lib_dirs: /usr/lib/x86_64-linux-gnu

Python deps:
    Cython: 0.28.5
     scipy: 1.2.0
setuptools: 39.0.1
       pip: 19.0.1
     numpy: 1.16.0
    pandas: 0.23.1
   sklearn: 0.20.2
```