Voting estimator will fail at fit if weights are passed and an estimator is None  
Because we don’t check for an estimator to be `None` in `sample_weight` support, `fit` is failing.  

To reproduce the problem, load the Iris dataset and build a VotingClassifier with two components—a logistic regression and a random forest. First, fit this classifier with a uniform array of sample weights so that both estimators train normally. Then disable the logistic regression by setting its entry to `None` and call `fit` again with the same sample weights. You would expect the classifier to skip the missing estimator and complete successfully, but it instead raises the following error:

```
AttributeError: 'NoneType' object has no attribute 'fit'
```