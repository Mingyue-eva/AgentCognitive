Unicode method names cause UnicodeDecodeError for some requests in Python 2.7.2  
The following example works fine:

```
files = {u'file': open(u'/usr/bin/diff', u'rb')}
response = requests.request(method='POST', url=u'http://httpbin.org/post', files=files)
```

But the following example (using `method=u'POST'` instead of `method='POST'`) produces a UnicodeDecodeError:

```
files = {u'file': open(u'/usr/bin/diff', u'rb')}
response = requests.request(method=u'POST', url=u'http://httpbin.org/post', files=files)
```

When this runs, Requests ends up mixing unicode and byte strings while building the HTTP message. httplib then tries to decode a non-ASCII byte (0xCF) as ASCII during header/body concatenation and raises a UnicodeDecodeError because that byte isn’t in the ASCII range.

My guess is that `u'POST'` is infecting the header with unicode when it should be a byte string. This is because `sessions.py:313` is simply:

```
req.method = method.upper()
```

My requests version is 1.2.3, but I see the same `.upper()` being used in the current source.