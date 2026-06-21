Please support header rows in RestructuredText output

### Description

It would be great if the following would work:

```Python
>>> from astropy.table import QTable
>>> import astropy.units as u
>>> import sys
>>> tbl = QTable({'wave': [350,950]*u.nm, 'response': [0.7, 1.2]*u.count})
>>> tbl.write(sys.stdout, format="ascii.rst")
===== ========
 wave response
===== ========
350.0      0.7
950.0      1.2
===== ========
>>> tbl.write(sys.stdout, format="ascii.fixed_width", header_rows=["name", "unit"])
|  wave | response |
|    nm |       ct |
| 350.0 |      0.7 |
| 950.0 |      1.2 |
>>> tbl.write(sys.stdout, format="ascii.rst", header_rows=["name", "unit"])
```
This call fails with a TypeError indicating that the RST writer’s constructor does not accept a `header_rows` keyword argument.