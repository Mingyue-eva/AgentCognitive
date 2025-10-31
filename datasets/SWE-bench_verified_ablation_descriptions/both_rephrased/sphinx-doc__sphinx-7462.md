`IndexError: pop from empty list` for empty tuple type annotation

**Describe the bug**  
When a function is annotated to return an empty tuple using the syntax for an empty Tuple type, Sphinx’s Python domain code tries to remove an element from a list that has no items and raises an IndexError indicating it cannot pop from an empty list.

**To Reproduce**  
Create a Python module containing a function whose return type is annotated as an empty tuple. Configure that module to be included by Sphinx’s autodoc extension. Make sure you have Sphinx (version 2.0.1 or higher) and the Read the Docs theme (version 0.4.3 or higher) installed. Then run the normal Sphinx build process. The documentation build will fail with the IndexError described above.

**Expected behavior**  
Docs are built and there is `foo` with valid type annotations.

**Your project**  
https://github.com/lycantropos/robust/tree/1c7b74e0cc39c1843a89583b8c245f08039a3978

**Environment info**  
- OS: Windows 10, but also reproduces on [readthedocs](https://readthedocs.org/projects/shewchuk/builds/10817256/).  
- Python version: 3.8.0  
- Sphinx version: 3.0.1  
- Sphinx extensions:  `['sphinx.ext.autodoc', 'sphinx.ext.viewcode']`