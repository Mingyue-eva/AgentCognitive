Pytest crashes the interpreter on debug build for 3.8+  
Short reproducer  
>>> Expression.compile("False")  
At runtime, the Python interpreter aborts with an assertion failure in compiler_nameop (compile.c:3559) because it rejects the name "False" in that context, causing the process to terminate and produce a core dump.  
Related issue for improvement of this behavior: [bpo-40870](https://bugs.python.org/issue40870)