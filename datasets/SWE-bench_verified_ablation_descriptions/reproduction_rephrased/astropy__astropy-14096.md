## Issue Description
Subclassed SkyCoord gives misleading attribute access message  
I'm trying to subclass `SkyCoord` and add a custom property. To reproduce the issue, I define a subclass called `custom_coord` in which the property `prop` simply returns `self.random_attr`. I then create an instance of this subclass with valid RA and Dec strings and ask for its `prop` attribute. Because `random_attr` doesn’t exist, accessing `prop` fails—but the error message incorrectly reports that `prop` itself is missing rather than pointing out the real problem with `random_attr`.

raises
```
Traceback (most recent call last):
  File "test.py", line 11, in <module>
    c.prop
  File "/Users/dstansby/miniconda3/lib/python3.7/site-packages/astropy/coordinates/sky_coordinate.py", line 600, in __getattr__
    .format(self.__class__.__name__, attr))
AttributeError: 'custom_coord' object has no attribute 'prop'
```