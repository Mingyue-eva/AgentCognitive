exception serialization should include chained exceptions

When run without xdist it displays the whole exception trace nicely, but when run with xdist it just displays the last one.

my setup:
pytest 4.0.2
pytest-xdist 1.25.0