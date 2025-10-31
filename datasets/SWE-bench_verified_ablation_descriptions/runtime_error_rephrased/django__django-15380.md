Migration autodetector crashes when renaming a model and field in a single step:
$ python manage.py makemigrations  
Did you rename the test_one.MyModel model to MyModel2? [y/N] y  
After confirming the rename, makemigrations raises a KeyError because it attempts to look up the old model name test_one.MyModel in its internal state and cannot find it.  
Reported by HoskeOwl.  
Regression in aa4acc164d1247c0de515c959f7b09648b57dc42.