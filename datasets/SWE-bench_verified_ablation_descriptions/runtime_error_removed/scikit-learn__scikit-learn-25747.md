## Issue Description
FeatureUnion not working when aggregating data and pandas transform output selected

### Describe the bug
I would like to use `pandas` transform output and use a custom transformer in a feature union which aggregates data. When I'm using this combination I got an error. When I use default `numpy` output it works fine.

### Steps/Code to Reproduce
```python
import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn import set_config
from sklearn.pipeline import make_union

index = pd.date_range(start="2020-01-01", end="2020-01-05", inclusive="left", freq="H")
data = pd.DataFrame(index=index, data=[10] * len(index), columns=["value"])
data["date"] = index.date

class MyTransformer(BaseEstimator, TransformerMixin):
    def fit(self, X: pd.DataFrame, y: pd.Series | None = None, **kwargs):
        return self

    def transform(self, X: pd.DataFrame, y: pd.Series | None = None) -> pd.DataFrame:
        return X["value"].groupby(X["date"]).sum()

# This works.
set_config(transform_output="default")
print(make_union(MyTransformer()).fit_transform(data))

# This does not work.
set_config(transform_output="pandas")
print(make_union(MyTransformer()).fit_transform(data))
```

### Expected Results
No error is thrown when using `pandas` transform output.

### Actual Results

### Versions
```shell
System:
    python: 3.10.6 (main, Aug 30 2022, 05:11:14) [Clang 13.0.0 (clang-1300.0.29.30)]
executable: /Users/macbookpro/.local/share/virtualenvs/3e_VBrf2/bin/python
   machine: macOS-11.3-x86_64-i386-64bit

Python dependencies:
      sklearn: 1.2.1
          pip: 22.3.1
   setuptools: 67.3.2
        numpy: 1.23.5
        scipy: 1.10.1
       Cython: None
       pandas: 1.4.4
   matplotlib: 3.7.0
       joblib: 1.2.0
threadpoolctl: 3.1.0

Built with OpenMP: True

threadpoolctl info:
       user_api: blas
   internal_api: openblas
         prefix: libopenblas
       filepath: /Users/macbookpro/.local/share/virtualenvs/3e_VBrf2/lib/python3.10/site-packages/numpy/.dylibs/libopenblas64_.0.dylib
        version: 0.3.20
threading_layer: pthreads
   architecture: Haswell
    num_threads: 4

       user_api: openmp
   internal_api: openmp
         prefix: libomp
       filepath: /Users/macbookpro/.local/share/virtualenvs/3e_VBrf2/lib/python3.10/site-packages/sklearn/.dylibs/libomp.dylib
        version: None
    num_threads: 8

       user_api: blas
   internal_api: openblas
         prefix: libopenblas
       filepath: /Users/macbookpro/.local/share/virtualenvs/3e_VBrf2/lib/python3.10/site-packages/scipy/.dylibs/libopenblas.0.dylib
        version: 0.3.18
threading_layer: pthreads
   architecture: Haswell
    num_threads: 4
```