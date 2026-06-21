Description

Migration autodetector crashes when renaming a model and field in a single step:

Reproduction

To reproduce the problem, change the name of the model called MyModel in the test_one app to MyModel2 and at the same time rename one of its fields. Then invoke Django’s migration creation (for example via makemigrations). When prompted to confirm the model rename, answer yes. Instead of generating a migration file, the process aborts.

Runtime error

As soon as the rename is confirmed, Django’s migration autodetector encounters an internal lookup failure: it can no longer find the original model in its in-memory representation and raises an unexpected key lookup error, causing the command to crash.

Reported by HoskeOwl.  
Regression in aa4acc164d1247c0de515c959f7b09648b57dc42.