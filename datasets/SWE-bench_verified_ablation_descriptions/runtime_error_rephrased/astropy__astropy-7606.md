Unit equality comparison with None raises TypeError for UnrecognizedUnit
```
In [12]: x = u.Unit('asdf', parse_strict='silent')

In [13]: x == None  # Should be False

A TypeError is raised because None is not recognized as a valid Unit.
```