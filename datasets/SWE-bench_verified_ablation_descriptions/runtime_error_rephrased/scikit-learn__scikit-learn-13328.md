## Issue Description
TypeError when supplying a boolean X to HuberRegressor fit

#### Description
`TypeError` when fitting `HuberRegressor` with boolean predictors.

#### Steps/Code to Reproduce

```python
import numpy as np
from sklearn.datasets import make_regression
from sklearn.linear_model import HuberRegressor

# Random data
X, y, coef = make_regression(n_samples=200, n_features=2, noise=4.0, coef=True, random_state=0)
X_bool = X > 0
X_bool_as_float = np.asarray(X_bool, dtype=float)
```

```python
# Works
huber = HuberRegressor().fit(X, y)
# Fails (!)
huber = HuberRegressor().fit(X_bool, y)
# Also works
huber = HuberRegressor().fit(X_bool_as_float, y)
```

#### Expected Results
No error is thrown when `dtype` of `X` is `bool` (`.fit(X_bool, y)`), since boolean arrays should be cast to float just like in `LinearRegression`.

#### Actual Results
When calling `HuberRegressor().fit` on a boolean feature matrix, the optimizer encounters a boolean mask and tries to negate it with the `-` operator. NumPy does not allow negation of boolean arrays using `-` and raises a `TypeError` suggesting the use of the `~` operator or `logical_not` instead.