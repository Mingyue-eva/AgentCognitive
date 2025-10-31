Naming a dimension "method" throws error when calling ".loc".

The name of the dimension should be irrelevant. The error suggests that at some point the dimensions are passed to another method in unsanitized form.

Edit: Updated to xarray 0.12 from conda-forge channel. The bug is still present.