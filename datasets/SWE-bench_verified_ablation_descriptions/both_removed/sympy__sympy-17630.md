Exception when multiplying BlockMatrix containing ZeroMatrix blocks

When a block matrix with zero blocks is defined, block-multiplying it once works, but block-multiplying it twice throws an exception. This seems to be caused by the zeros in the intermediate result being Zero instead of ZeroMatrix.

I don’t understand SymPy internals well enough to find out why this happens. I use Python 3.7.4 and sympy 1.4 (installed with pip).