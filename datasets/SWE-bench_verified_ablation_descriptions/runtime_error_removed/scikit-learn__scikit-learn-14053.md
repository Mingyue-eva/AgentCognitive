## Issue Description
export_text returns incorrect output when the tree only has one feature

#### Description
`export_text` does not handle the single‐feature case properly.

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

#### Versions
```
System:
    python: 3.7.3 [MSC v.1915 64 bit (AMD64)]
    machine: Windows-10-10.0.17763-SP0

Python deps:
       pip: 19.1
setuptools: 41.0.0
   sklearn: 0.21.1
     numpy: 1.16.2
     scipy: 1.2.1
    Cython: 0.29.7
    pandas: 0.24.2
```