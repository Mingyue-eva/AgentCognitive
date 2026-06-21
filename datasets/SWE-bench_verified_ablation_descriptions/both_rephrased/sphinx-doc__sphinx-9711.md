needs_extensions checks versions using strings

### Describe the bug

The `needs_extensions` check is handy for verifying minimum extension versions, but it only checks versions in a “string-like” manner. This means any version greater than 9 is not allowed for any check of something greater than 1. That is, it treats '0.6' as greater than '0.10' when compared as strings, even though as version numbers 0.6 is less than 0.10. Since Sphinx uses string comparison, some extension versions may be rejected when they should be accepted.

### How to Reproduce

First, clone the mplcursors repository and install its documentation requirements. Then install the project in editable mode and run the HTML documentation build. With sphinx-gallery locked at version 0.9, the build completes successfully. Next, upgrade sphinx-gallery to version 0.10.0 and run the documentation build again. At this point, the build fails because during the build process Sphinx complains that the sphinx_gallery.gen_gallery extension does not meet the minimum required version of 0.6.0, even though version 0.10.0 is installed.

### Expected behavior

sphinx-gallery 0.10.0 should be accepted if 0.6 is the minimum specified.

### Your project

https://github.com/anntzer/mplcursors

### Screenshots

_No response_

### OS

Fedora

### Python version

3.9.6

### Sphinx version

4.1.2

### Sphinx extensions

_No response_

### Extra tools

_No response_

### Additional context

_No response_