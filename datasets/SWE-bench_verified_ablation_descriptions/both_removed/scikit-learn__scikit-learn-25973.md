Unable to pass splits to SequentialFeatureSelector

Describe the bug

This runs fine with e.g. `cv=5`, but according to the documentation, it should also be able to take an iterable of splits. However, passing splits from the cross validator fails. I’m fairly certain I have done similar things in the past to other classes in scikit-learn requiring a `cv` parameter. If somebody could confirm whether this is a bug, or I’m doing something wrong, that would be great. Sorry if this is unneeded noise in the feed.

Versions

1.2.2