TypeError when supplying a boolean X to HuberRegressor fit

Description  
TypeError when fitting HuberRegressor with boolean predictors. Boolean array inputs should be converted to float internally, as is done by LinearRegression, but HuberRegressor raises a TypeError for boolean arrays.