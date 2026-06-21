## Issue Description
Merging dataArray into dataset using dataset method fails  
While it's possible to merge a dataset and a dataarray object using the top-level `merge()` function, if you try the same thing with the `ds.merge()` method it fails.

```python
import xarray as xr

ds = xr.Dataset({'a': 0})
da = xr.DataArray(1, name='b')

expected = xr.merge([ds, da])  # works fine
print(expected)

ds.merge(da)  # fails
```

When calling `ds.merge(da)`, the code raises an AttributeError because the merge logic tries to call `items()` on each input object, and `DataArray` does not implement an `items` method.