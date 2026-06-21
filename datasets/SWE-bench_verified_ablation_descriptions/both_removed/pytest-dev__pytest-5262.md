_pytest.capture.EncodedFile mode should not include `b`

Exception when youtube-dl logs to pytest captured output. Youtube-dl looks for `b` in out.mode to decide whether to write bytes or str. _pytest.capture.EncodedFile incorrectly advertises rb+, the mode of the underlying stream. Its write() method raises an exception when passed bytes.