_pytest.capture.EncodedFile mode should not include `b` (binary)

<!--
Thanks for submitting an issue!

Here's a quick checklist for what to provide:
-->

- [x] a detailed description of the bug or suggestion

Exception when youtube-dl logs to pytest captured output. Youtube-dl looks for `b` in `out.mode` to decide whether to writes `bytes` or `str`. `_pytest.capture.EncodedFile` incorrectly advertises `rb+`, the mode of the underlying stream. Its `write()` method raises an exception when passed `bytes`.

- [x] Steps to reproduce and expected outcome

To reproduce this issue, install pytest and youtube-dl in a fresh environment, create a test file that defines a single test function which imports youtube_dl and calls its extract_info method on any URL, and then run pytest against that file. You would expect the test to run without error and for youtube-dl’s progress messages to appear normally.

- [x] What happened when the error occurred

When the test is run, pytest reports one collected item and then fails. The failure happens because youtube-dl writes a bytes object into the captured output stream, but the `_pytest.capture.EncodedFile` object, despite advertising a binary mode, only accepts text. As a result, a TypeError is raised stating that the write argument must be a string rather than bytes.

- [x] output of `pip list` from the virtual environment you are using
```
Package        Version  
-------------- ---------
atomicwrites   1.3.0    
attrs          19.1.0   
more-itertools 7.0.0    
pip            19.1.1   
pluggy         0.11.0   
py             1.8.0    
pytest         4.5.0    
setuptools     41.0.1   
six            1.12.0   
wcwidth        0.1.7    
wheel          0.33.4   
youtube-dl     2019.5.11
```

- [x] pytest and operating system versions
```
This is pytest version 4.5.0, imported from /private/tmp/pytest-issue-ve3/lib/python3.7/site-packages/pytest.py
```
```
macOS 10.14.4 (18E226)
```

- [x] minimal example if possible

You can reproduce the problem by creating a file named `test.py` with a test that calls `youtube_dl.YoutubeDL().extract_info` on a URL, then running pytest in an environment where both pytest and youtube-dl are installed.