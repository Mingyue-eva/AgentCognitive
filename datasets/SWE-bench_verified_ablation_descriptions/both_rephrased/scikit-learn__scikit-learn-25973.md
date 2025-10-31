Unable to pass splits to SequentialFeatureSelector

### Describe the bug

This runs fine with e.g. `cv=5`, but according to the documentation, it should also be able to take an iterable of splits. However, passing splits from the cross validator fails

I’m fairly certain I have done similar things in the past to other classes in scikit-learn requiring a `cv` parameter.

If somebody could confirm whether this is a bug, or I’m doing something wrong, that would be great. Sorry if this is unneeded noise in the feed.

### Steps to Reproduce

First, generate a synthetic classification dataset with default parameters. Then create a group label array where the first half of the samples belong to group 0 and the second half belong to group 1. Use a LeaveOneGroupOut cross-validator to produce an iterable of train/test split indices based on those group labels. Next, instantiate a K-nearest neighbors classifier with five neighbors and pass it to a SequentialFeatureSelector configured to pick five features and use accuracy as the scoring metric, supplying the custom split iterator as the cross-validation argument. Finally, call the selector’s `fit` method on the dataset and target labels.

### Expected Results

The feature selector should complete without any errors and return a fitted object.

### Actual Results

As soon as the fitting process starts, an IndexError is raised indicating that a list index is out of range, and the feature selection does not proceed.

### Versions

1.2.2