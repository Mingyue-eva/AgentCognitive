Voting estimator will fail at fit if weights are passed and an estimator is None  
Because we don't check for an estimator to be None in sample_weight support, fit is failing.

To reproduce the issue, first train a voting classifier composed of a logistic regression and a random forest on the iris dataset while supplying uniform sample weights. That fit completes successfully. Then remove the logistic regression estimator by setting it to None and try fitting the voting classifier again with the same sample weights. At this point, the fitting process still attempts to call methods on the disabled estimator and fails.

The expected outcome is that the voting classifier would detect the missing estimator and either skip it or otherwise handle its absence so that fitting with sample weights still succeeds without error.

When the second fit is invoked after disabling one of the estimators, an attribute error arises because the code tries to call the fit method on a NoneType object, causing the operation to crash.