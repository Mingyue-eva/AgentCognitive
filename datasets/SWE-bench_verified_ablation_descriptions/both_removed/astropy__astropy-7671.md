minversion failures

The change in PR #7647 causes minversion to fail in certain cases.  
Apparently this is due to a bug in LooseVersion (https://bugs.python.org/issue30272).  
Note that without the “.3” it doesn’t fail.  
Using pkg_resources.parse_version (which was removed) works.  

CC: @mhvk