Should `Quantity.__array_ufunc__()` return `NotImplemented` instead of raising `ValueError` if the inputs are incompatible?

### Description
I'm trying to implement a duck type of `astropy.units.Quantity`. If you are interested, the project is available https://github.com/Kankelborg-Group/named_arrays. I'm running into trouble trying to coerce my duck type to use the reflected versions of the arithmetic operators if the left operand is not an instance of the duck type _and_ they have equivalent but different units. Consider the following minimal working example of my duck type.

In this example, I define a simple wrapper around an `astropy.units.Quantity` by subclassing `numpy.lib.mixins.NDArrayOperatorsMixin`. The wrapper holds an internal `Quantity`, exposes its unit via a `unit` property, and implements `__array_ufunc__` so that:

- Any wrapped inputs are unwrapped to their internal `Quantity`.
- For each input that becomes a NumPy array or `Quantity`, I delegate to its own `__array_ufunc__`.
- If that delegation returns something other than `NotImplemented`, I wrap the result back into my duck type.

Reproduction:
1. Create an instance of the wrapper holding a quantity of 1 mm.
2. Add that wrapper to a standard astropy `Quantity` of 1 m (wrapper on the left, standard quantity on the right).
3. Observe that the addition succeeds and produces a new wrapper holding the correct summed quantity.
4. Do the reverse (standard quantity on the left, wrapper on the right) when both share the same unit—this also succeeds.
5. Finally, attempt to add a standard astropy `Quantity` of 1 m (left operand) to your wrapper holding 1 mm (right operand).

Expected Result:
The addition should be handled by the reflected operator on the wrapper and should return a wrapper representing 1.001 m.

Runtime Error:
Instead of falling back to the wrapper’s reflected addition, astropy’s ufunc handling tries to convert the wrapper object into a plain numeric array. Because the wrapper is neither a basic scalar nor a native array, the conversion check fails and astropy raises a `ValueError` indicating that the value is not scalar-compatible or convertible to an int, float, or complex array. This prevents the reflected addition from ever being called.

I would argue that `Quantity.__array_ufunc__()` should really return `NotImplemented` in this instance, since it would allow for `__radd__` to be called instead of the error being raised. I feel that the current behavior is also inconsistent with the numpy docs which specify that `NotImplemented` should be returned if the requested operation is not implemented.

What does everyone think?  I am more than happy to open a PR to try and solve this issue if we think it's worth pursuing.