## Issue Description
`IndexError: pop from empty list` for empty tuple type annotation

**Describe the bug**
Following the notation for an empty tuple from this mypy issue:

```python
from typing import Tuple

def foo() -> Tuple[()]:
    """Sample text."""
    return ()
```

I get:

```bash
  File "\path\to\site-packages\sphinx\domains\python.py", line 112, in unparse
    result.pop()
IndexError: pop from empty list
```

**To Reproduce**
I created a simple Python module defining a function `foo` that returns an empty tuple with the annotation `Tuple[()]` and included it in my Sphinx documentation source. In the project’s `docs/requirements.txt`, I specified Sphinx version 2.0.1 or higher and the Read the Docs theme version 0.4.3 or higher. Then I ran the Sphinx build command to generate the documentation.

**Expected behavior**
The documentation build should complete without errors and the generated docs should include the `foo` function with its empty-tuple return type correctly rendered.

**Your project**
https://github.com/lycantropos/robust/tree/1c7b74e0cc39c1843a89583b8c245f08039a3978

**Environment info**
- OS: Windows 10, but also reproduces on Read the Docs  
- Python version: 3.8.0  
- Sphinx version: 3.0.1  
- Sphinx extensions: `['sphinx.ext.autodoc', 'sphinx.ext.viewcode']`