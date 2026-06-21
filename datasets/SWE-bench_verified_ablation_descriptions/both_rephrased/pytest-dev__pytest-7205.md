BytesWarning when using --setup-show with bytes parameter

To reproduce this issue, run pytest under Python 3.8.2 with the -bb flag (so ByteWarnings are treated as errors) and the --setup-show option on a test that is parameterized with a bytes value (for example, passing in b'Hello World'). The expected behavior is that pytest should print the setup step for the data fixture and display the byte parameter in a safe, readable form without raising any warnings.

At setup time, pytest tries to convert the bytes parameter to a string for display, which raises a BytesWarning. Because the -bb flag turns warnings into errors, the test run is aborted when it encounters this warning, instead of completing successfully.

Shouldn’t that be using saferepr or something rather than (implicitly) str()?