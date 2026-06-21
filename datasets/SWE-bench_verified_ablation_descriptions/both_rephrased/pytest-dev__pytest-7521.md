pytest 6.0.0rc1: capfd.readouterr() converts \r to \n  
I am testing pytest 6.0.0rc1 with Fedora packages. This is the first failure I get, from borgbackup 1.1.13.

To reproduce the issue, I simulate a very narrow terminal by setting the COLUMNS environment variable to “4” and LINES to “1.” Then I create a ProgressIndicatorPercent object for 1 000 total units, configured to update every five units and formatted as a three-digit percentage. When I invoke its show method at zero progress and capture the output, I expect the log line to end with a carriage return so that it stays on the same line, but instead I see a newline at the end.

A minimal demonstration is to print any message with end set to a carriage return, capture the output with capfd.readouterr(), and verify that the captured string still ends with '\r'. Under pytest 5 this works exactly as expected—the carriage return is preserved. Under pytest 6, however, the captured output ends with '\n' instead, causing the assertion that checks for '\r' at the end to fail.

This is Fedora 32 with Python 3.8 (the original failure in borgbackup is Fedora 33 with Python 3.9).

I could have not found anything about this change in the changelog nor at https://docs.pytest.org/en/latest/capture.html hence I assume this is a regression. I've labeled it as such, but feel free to change that.