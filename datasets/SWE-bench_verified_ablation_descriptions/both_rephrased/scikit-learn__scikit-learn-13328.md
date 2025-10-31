#### Description
A `TypeError` occurs when attempting to fit a `HuberRegressor` using predictors that are stored in a boolean array.

#### Steps to Reproduce
First, generate a synthetic regression dataset with two input features and a continuous target. Next, create a boolean feature matrix by testing whether each entry in the original feature matrix is greater than zero. Then, fit a `HuberRegressor` to the original floating‐point data and observe that it completes without error. After that, fit the same model using the boolean feature matrix and observe the failure. Finally, convert the boolean matrix to floating‐point values and fit the model again, noting that it succeeds once more.

#### Expected Results
No error should occur when the feature matrix consists of boolean values. The regressor should implicitly convert those booleans to floats before proceeding, just as it does with other estimators like `LinearRegression`.

#### Actual Results
When calling `.fit` with the boolean array, the fitting process aborts with a type error inside the internal loss‐and‐gradient routine. The failure arises because the code attempts to apply the unary minus operator to a boolean array, which NumPy does not allow. The message suggests using the bitwise NOT operator (`~`) or the `logical_not` function instead.

#### Versions

Latest versions of everything as far as I am aware:

```python
import sklearn
sklearn.show_versions() 
```

```
System:
    python: 3.7.2 (default, Jan 10 2019, 23:51:51)  [GCC 8.2.1 20181127]
executable: /home/saulius/.virtualenvs/newest-sklearn/bin/python
   machine: Linux-4.20.10-arch1-1-ARCH-x86_64-with-arch

BLAS:
    macros: NO_ATLAS_INFO=1, HAVE_CBLAS=None
  lib_dirs: /usr/lib64
cblas_libs: cblas

Python deps:
       pip: 19.0.3
setuptools: 40.8.0
   sklearn: 0.21.dev0
     numpy: 1.16.2
     scipy: 1.2.1
    Cython: 0.29.5
    pandas: None
```