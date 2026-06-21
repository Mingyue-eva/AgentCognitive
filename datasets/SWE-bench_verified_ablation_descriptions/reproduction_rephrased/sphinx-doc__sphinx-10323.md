## Issue Description
Use of literalinclude prepend results in incorrect indent formatting for code examples

### Describe the bug

Cannot determine a mechanism to use literalinclude directive with `prepend` or `append` to match code example indentation, as leading whitespace is removed.

### How to Reproduce

In a Sphinx project we have an `index.rst` file where we use a `.. literalinclude:: pom.xml` directive, set the language to XML, supply a `:prepend:` value of several spaces plus `</plugin>`, and constrain the inclusion to the lines between `<groupId>com.github.ekryd.sortpom</groupId>` and `</plugin>`. The referenced `pom.xml` defines a Maven project whose `<build>` section contains two `<plugin>` entries: one for the compiler plugin and one for the SortPom plugin. When Sphinx processes the directive, it correctly extracts the second plugin block but emits the opening `<plugin>` tag at the left margin with no leading spaces, then indents the nested elements, and finally misplaces the closing tag, rather than preserving the same indentation level that appears in the source file.

### Expected behavior

The snippet should retain its original leading whitespace so that the `<plugin>` tag and its inner elements stay indented exactly as they do in `pom.xml`, producing a properly aligned code fragment.

### Your project

https://github.com/geoserver/geoserver/tree/main/doc/en/developer/source

### Screenshots

_No response_

### OS

Mac

### Python version

3.9.10

### Sphinx version

4.4.0

### Sphinx extensions

['sphinx.ext.todo', 'sphinx.ext.extlinks']

### Extra tools

_No response_

### Additional context

Using `dedent` creatively almost provides a workaround:

``` rst
.. literalinclude:: pom.xml
   :language: xml
   :start-at: <groupId>com.github.ekryd.sortpom</groupId>
   :end-before: </plugin>
   :prepend: _____</plugin>
   :dedent: 5
```

Produces a warning, which fails the build with ``-W`` build policy.
```
index.rst.rst:155: WARNING: non-whitespace stripped by dedent
```