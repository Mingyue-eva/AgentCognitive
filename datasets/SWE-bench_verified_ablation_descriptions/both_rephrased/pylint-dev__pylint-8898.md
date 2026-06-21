bad-names-rgxs mangles regular expressions with commas

### Bug description

Since pylint splits on commas in this option, instead of taking a list of strings, if there are any commas in the regular expression, the result is mangled before being parsed. The config below demonstrates this clearly by causing pylint to crash immediately.

### Configuration and reproduction

To reproduce the problem, configure pylint’s bad-name-rgxs option with a pattern that includes a comma—for example, a capture group with a quantifier range—and then invoke pylint on any Python file (for instance, running pylint against foo.py). As soon as pylint reads that option, it will attempt to compile the malformed pattern and abort before linting the file.

### Error observed

When pylint processes the mangled pattern, it terminates with an error indicating that a closing parenthesis is missing and that the subpattern is unterminated, preventing any further analysis.

### Expected behavior

I would expect any valid regular expression to be expressible in this option. If not directly, adding some way to escape commas so that this issue can be worked around.

### Pylint version

pylint 2.14.4  
astroid 2.11.7  
Python 3.10.4 (main, Apr  2 2022, 09:04:19) [GCC 11.2.0]

### OS / Environment

Pop! OS 22.04

### Additional dependencies

_No response_