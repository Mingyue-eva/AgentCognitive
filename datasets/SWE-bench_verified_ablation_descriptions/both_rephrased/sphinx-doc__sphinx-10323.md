## Task Objective  
You are given a software issue description that may include both:  
1. Detailed reproduction steps or executable test code, along with the expected output.  
2. Executable code that triggers a runtime error, including the corresponding error message or stack trace.  

Your task is to rewrite **both** portions into natural language explanations as a human developer might express them, clearly conveying the reproduction process and expected result.

- For reproduction: Describe how to trigger the issue and what the expected outcome is, without using code.  
- For runtime error: Describe what kind of error occurred, when it happened, and what was observed — without including stack traces or raw exception messages.  

Leave the rest of the issue description unchanged.

---

Use of literalinclude prepend results in incorrect indent formatting for code eamples

### Describe the bug

Cannot determine a mechanism to use literalinclude directive with `prepend` or `append` to match code example indentation, as leading whitespace is removed.

### How to Reproduce

When you include a section of your XML file in a reStructuredText document using the literalinclude directive, you specify start and end markers around the `<plugin>` element and add a `prepend` option to insert the closing tag at the beginning of the snippet. In practice, the inserted closing tag loses all of its leading spaces, so the entire code example shifts to the left and appears misaligned compared to the rest of your document.

### Expected behavior

Expect leading white space to be preserved in output:

```xml
      <plugin>
        <groupId>com.github.ekryd.sortpom</groupId>
        <artifactId>sortpom-maven-plugin</artifactId>
        <version>2.15.0</version>
        <configuration>
          <verifyFailOn>strict</verifyFailOn>
        </configuration>
      </plugin>
```

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

I attempted to work around the problem by using the `dedent` option to strip a fixed number of spaces from the included snippet before adding my `prepend` text. During the documentation build, I received a warning indicating that non-whitespace characters were being removed by the dedent process. Because our build treats warnings as errors, this warning caused the entire build to fail. Ideally, dedent should only affect the included file’s indentation and not alter the text provided via `prepend` or `append`.