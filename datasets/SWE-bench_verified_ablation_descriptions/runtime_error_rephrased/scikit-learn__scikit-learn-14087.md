## Issue Description
IndexError thrown with LogisticRegressionCV and refit=False

#### Description
The following error is thrown when trying to estimate a regularization parameter via cross-validation, *without* refitting.

#### Steps/Code to Reproduce
```python
import sys
import sklearn
from sklearn.linear_model import LogisticRegressionCV
import numpy as np

np.random.seed(29)
X = np.random.normal(size=(1000, 3))
beta = np.random.normal(size=3)
intercept = np.random.normal(size=None)
y = np.sign(intercept + X @ beta)

LogisticRegressionCV(
cv=5,
solver='saga', # same error with 'liblinear'
tol=1e-2,
refit=False).fit(X, y)
```

#### Expected Results
No error is thrown. 

#### Actual Results
When fitting with refit=False, the code attempts to average coefficient paths across the cross-validation folds by indexing into the array with too many dimensions, which raises an IndexError indicating “too many indices for array.”