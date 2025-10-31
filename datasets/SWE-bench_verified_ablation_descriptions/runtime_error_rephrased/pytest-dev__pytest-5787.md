exception serialization should include chained exceptions
given some simple tests:
```
def test_chained_exception_with_from():
    try:
        try:
            raise ValueError(11)
        except Exception as e1:
            raise ValueError(12) from e1
    except Exception as e2:
        raise ValueError(13) from e2


def test_chained_exception_without_from():
    try:
        try:
            raise ValueError(21)
        except Exception:
            raise ValueError(22)
    except Exception:
        raise ValueError(23)
```
when run without xdist it displays whole exception trace nicely:

In test_chained_exception_with_from, a ValueError(11) is raised first, then a ValueError(12) is raised explicitly from that first exception, and finally a ValueError(13) is raised from the second; pytest shows the entire chain with “The above exception was the direct cause of the following exception” between each. In test_chained_exception_without_from, a ValueError(21) occurs, a ValueError(22) is raised during its handling, and finally a ValueError(23) is raised, with pytest reporting all three exceptions and indicating that each subsequent error happened while handling the previous one.

but when run with xdist (`-n auto`), it just displays the last one:

Only the final ValueError(13) from test_chained_exception_with_from and the final ValueError(23) from test_chained_exception_without_from are reported, without any of the intermediate chained context.

my setup:
```
pytest           4.0.2       
pytest-xdist     1.25.0
```