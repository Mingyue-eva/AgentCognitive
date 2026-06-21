5.1.2 ImportError while loading conftest (windows import folder casing issues)  
5.1.1 works fine. after upgrade to 5.1.2, the path was converted to lower case  

I upgraded pytest from version 5.1.1 to 5.1.2 and then ran the tests in my project’s Python directory using the --collect-only flag with the smoke marker against the PIsys folder. I expected pytest to enumerate all tests in that folder without error.

ImportError while loading conftest 'c:\azure\kms\componenttest\python\pisys\conftest.py'.  
ModuleNotFoundError: No module named 'python'  
PS C:\Azure\KMS\ComponentTest\Python>