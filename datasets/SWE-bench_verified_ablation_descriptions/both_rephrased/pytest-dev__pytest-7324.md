Pytest crashes the interpreter on debug build for 3.8+

When you run a debug‐built Python 3.8 or later in interactive mode, create an AST expression from the literal False and then call its compile method. You would expect to get back a code object or a controlled exception, but instead the interpreter immediately aborts.

At runtime, an internal compiler assertion fails while checking that the name isn’t one of the special constants, causing the process to terminate and produce a core dump.

Related issue for improvement of this behavior: [bpo-40870](https://bugs.python.org/issue40870)