minversion failures  
The change in PR #7647 causes `minversion` to fail in certain cases, e.g.:  
```python
>>> from astropy.utils import minversion
>>> minversion('numpy', '1.14dev')
```

apparently because of a bug in LooseVersion (https://bugs.python.org/issue30272):

```python
>>> from distutils.version import LooseVersion
>>> LooseVersion('1.14.3') >= LooseVersion('1.14dev')
```

Note that without the “.3” it doesn't fail:

```python
>>> LooseVersion('1.14') >= LooseVersion('1.14dev')
False
```

and using pkg_resources.parse_version (which was removed) works:

```python
>>> from pkg_resources import parse_version
>>> parse_version('1.14.3') >= parse_version('1.14dev')
True
```

CC: @mhvk