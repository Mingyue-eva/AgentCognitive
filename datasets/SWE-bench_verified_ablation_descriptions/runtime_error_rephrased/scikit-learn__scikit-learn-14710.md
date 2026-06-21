#### Actual Results

When calling `gbrt.fit(X, y)`, the early‐stopping routine invokes the accuracy scorer with integer‐encoded true labels and the original string class predictions. NumPy’s union and sort operations then attempt to compare strings and floats, causing a TypeError complaining that “‘<’ not supported between instances of ‘str’ and ‘float’.”