units.quantity_input decorator fails for constructors with type hinted return value -> None

### Summary
I am using the `units.quantity_input` decorator with typing hints for constructors, however when I add the correct return value for the constructor (`None`) then I get an exception, because `None` has no attribute `to`.

### Reproducer
Define a class whose `__init__` method is decorated with `units.quantity_input`, require that the single argument be provided as a voltage quantity in volts, and annotate the constructor to return `None`. When you instantiate this class by passing a value of one volt, you would expect the object to be created successfully. Instead, at instantiation time the decorator tries to convert the constructor’s return value into a unit-aware quantity. Since the constructor actually returns `None`, the decorator’s attempt to call a unit conversion method fails.

This has been tested on Fedora 27 with Python 3.6.3, Astropy 2.0.2 and NumPy 1.13.3 all from Fedora’s repository.

### Workaround
The issue can be circumvented by not adding the return type typing hint. Unfortunately, then a static type checker cannot infer that this function returns nothing.

### Possible fix
Maybe the decorator could explicitly check whether None is returned and then omit the unit check.