## Issue Description
Linkcheck should report HTTP errors instead of Anchor not found

**Describe the bug**  
The `linkcheck` command always reports that it was unable to find the anchor when `linkcheck_anchors` is enabled, even when the server actually returned an error status code (for example 404 or 500). While it is true that the anchor cannot be found, the underlying problem is that the server responded with an error.

**To Reproduce**  
First, create a new Sphinx project named “proj” with separate source and build directories, author “me,” release “1.0,” and language “en.” Next, add a link to a non-existent file on an external server by inserting a reference to `https://google.com/test.txt#test` into your `source/index.rst` file. Finally, run the linkcheck builder (for example by running `make linkcheck`). Although the server responds with a 404 Not Found for that URL, Sphinx reports only that it could not find the anchor.

**Expected behavior**  
Actual result: linkcheck reports  
“broken https://google.com/test.txt#test – Anchor ‘test’ not found.”  
Expected result: linkcheck should treat the missing file as an HTTP error and report  
“broken https://google.com/test.txt#test – 404 Client Error: Not Found for url: https://google.com/test.txt,”  
just as it does when anchor checking is disabled.

**Environment info**  
- OS: Linux 5.8.12.a-1-hardened  
- Python version: 3.8.5  
- Sphinx version: 3.2.1