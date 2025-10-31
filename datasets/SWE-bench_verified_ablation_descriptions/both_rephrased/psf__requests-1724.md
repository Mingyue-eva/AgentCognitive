Unicode method names cause UnicodeDecodeError for some requests in Python 2.7.2

In the working scenario, you prepare a files dictionary by opening /usr/bin/diff in binary mode and assigning it to the key "file". You then call requests.request with method='POST' (a normal byte string) and a Unicode URL. The request completes successfully and you receive the expected HTTP response from httpbin.org.

If you repeat the same steps but pass the method argument as a Unicode string instead of a byte string, the library fails as soon as it attempts to send the headers and body. At that point, the underlying HTTP client tries to merge a Unicode header value with the raw multipart body and encounters a non-ASCII byte (0xCF). Because the default ASCII codec cannot decode that byte, a UnicodeDecodeError is raised and the request is aborted.

My guess is that u'POST' is infecting the header with unicode when it should be a string.  This is because sessions.py:313 is simply:

```
req.method = method.upper()
```

My requests version is 1.2.3, but I see the same `.upper()` being used in the current source.