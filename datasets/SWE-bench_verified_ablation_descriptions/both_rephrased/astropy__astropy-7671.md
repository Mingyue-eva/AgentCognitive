minversion failures  
The change in PR #7647 causes minversion to fail in certain cases, for example:

When you try to check that the installed NumPy package meets a minimum requirement of “1.14dev” by calling the minversion utility, you do not get back a simple True or False. Instead, the function immediately raises a TypeError.

apparently because of a bug in LooseVersion (https://bugs.python.org/issue30272):

When LooseVersion is asked to compare a full release version such as “1.14.3” against a development label like “1.14dev,” it ends up trying to compare an integer component against a string component. This triggers a TypeError complaining that the less-than operation is not supported between integer and string types.

Note that without the “.3” it doesn’t fail:

If you compare “1.14” to “1.14dev” using LooseVersion, it simply returns False as expected, without raising an error.

and using pkg_resources.parse_version (which was removed) works:

When the same version strings are compared with the parsing function from pkg_resources, the comparison succeeds and correctly reports that “1.14.3” is greater than or equal to “1.14dev.”

CC: @mhvk