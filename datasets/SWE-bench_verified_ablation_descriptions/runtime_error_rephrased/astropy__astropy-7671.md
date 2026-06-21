minversion failures  
The change in PR #7647 causes `minversion` to fail in certain cases, e.g.:  
>>> from astropy.utils import minversion  
>>> minversion('numpy', '1.14dev')  
This raises a TypeError because during the version comparison LooseVersion ends up trying to compare an integer component with a string, which isn’t supported.  

Apparently this is due to a bug in LooseVersion (https://bugs.python.org/issue30272):  
>>> from distutils.version import LooseVersion  
>>> LooseVersion('1.14.3') >= LooseVersion('1.14dev')  
This also triggers a TypeError for the same reason.  

Note that without the “.3” it doesn’t fail:  
>>> LooseVersion('1.14') >= LooseVersion('1.14dev')  
False  

and using pkg_resources.parse_version (which was removed) works:  
>>> from pkg_resources import parse_version  
>>> parse_version('1.14.3') >= parse_version('1.14dev')  
True  

CC: @mhvk  
