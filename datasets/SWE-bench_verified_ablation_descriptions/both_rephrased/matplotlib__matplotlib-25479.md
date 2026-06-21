Confusing (broken?) colormap name handling  
Consider the following example in which one creates and registers a new colormap and attempt to use it with the `pyplot` interface.

In this example, Matplotlib is imported and its version is confirmed to be 1.4.3. A small list of three RGB color triplets is defined and converted into a LinearSegmentedColormap object whose internal name is set to “some_cmap_name.” That colormap object is then registered under the name “my_cmap_name.”

Everything OK so far. Note the difference in the names `some_cmap_name` and `my_cmap_name`. Now when we try to use the new colormap things start to go wrong.

When the global colormap is set to “my_cmap_name” and a 2×2 array is displayed with `imshow`, Matplotlib raises an error indicating that the colormap “some_cmap_name” is not recognized among the available colormaps, despite the fact that “my_cmap_name” had been registered.

As seen from the error message, it's `my_cmap.name (=some_cmap_name)` that is looked up instead of the registered colormap name, `my_cmap_name`. Manually looking up `my_cmap_name` works just fine:

``` python
cm.get_cmap('my_cmap_name')
<matplotlib.colors.LinearSegmentedColormap at 0x7f4813e5dda0>
```

For this to work as I had expected, one has to make sure that the colormap name and the registered name are the same due to some sort of "double internal name lookup tables" in matplotlib.

I found this problem to be very confusing at first since I imported a colormap from another module, registered it, and tried to use it with no luck, e.g. something like:

``` python
from some_module import my_cmap
cm.register_cmap(name='my_cmap_name', cmap=my_cmap)
```

at which point, I expected to be able to refer to my newly registered colormap by the name `my_cmap_name`.