pytest 6.0.0rc1: capfd.readouterr() converts \r to \n  
I am testing pytest 6.0.0rc1 with Fedora packages. This is the first failure I get, from borgbackup 1.1.13.  

______________________ test_progress_percentage_sameline _______________________  
capfd = <_pytest.capture.CaptureFixture object at 0x7f9bd55e4d00>  
monkeypatch = <_pytest.monkeypatch.MonkeyPatch object at 0x7f9bcbbced60>  

    def test_progress_percentage_sameline(capfd, monkeypatch):  
        # run the test as if it was in a 4x1 terminal  
        monkeypatch.setenv('COLUMNS', '4')  
        monkeypatch.setenv('LINES', '1')  
        pi = ProgressIndicatorPercent(1000, step=5, start=0, msg="%3.0f%%")  
        pi.logger.setLevel('INFO')  
        pi.show(0)  
        out, err = capfd.readouterr()  
        assert err == '  0%\r'  

When this assertion runs, the captured stderr actually ends with a newline character rather than the expected carriage return, so the test fails because '\n' does not match '\r'.  

I’ve distilled a reproducer:  

def test_cafd_includes_carriage_return(capfd):  
    print('Greetings from DOS', end='\r')  
    out, err = capfd.readouterr()  
    assert out.endswith('\r')  

pytest 5 passed this test without issue. Under pytest 6.0.0rc1, the output is ‘Greetings from DOS\n’ instead of ending with ‘\r’, so the endswith('\r') check returns False and the assertion fails.