#### Description
`export_text` returns `IndexError` when there is a single feature.

#### Steps/Code to Reproduce
```python
from sklearn.tree import DecisionTreeClassifier
from sklearn.tree.export import export_text
from sklearn.datasets import load_iris

X, y = load_iris(return_X_y=True)
X = X[:, 0].reshape(-1, 1)

tree = DecisionTreeClassifier()
tree.fit(X, y)
tree_text = export_text(tree, feature_names=['sepal_length'])
print(tree_text)
```

#### Actual Results
When `export_text` runs on a tree with only one feature, it tries to access a feature name at an index that doesn’t exist in the provided list, causing an out-of-range error.