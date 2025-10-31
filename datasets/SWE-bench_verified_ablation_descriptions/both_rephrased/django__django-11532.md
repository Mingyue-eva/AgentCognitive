Email messages crash on non-ASCII domain when email encoding is non-unicode.

Description

When the computer hostname is set in unicode (in my case "正宗"), the following test fails: https://github.com/django/django/blob/master/tests/mail/tests.py#L368  
Specifically, since the encoding is set to iso-8859-1, Python attempts to convert all of the headers to that encoding, including the Message-ID header which has been set here: https://github.com/django/django/blob/master/django/core/mail/message.py#L260  
This is not just a problem in the tests, Django should be handling the encoding of the message properly

Reproduction
To trigger this issue, configure the system hostname to a Unicode string that cannot be represented in ISO-8859-1 (for example “正宗”). Then run the Django mail unit tests. The test expects Django to convert the domain portion of the Message-ID header into its punycode form (for example “xn--p8s937b”), but instead the header generation fails.

Fix
Have django.core.mail.utils or django.core.mail.message convert the domain name to punycode before using it.

Test
In the existing test, the DNS_NAME constant is temporarily replaced with the Unicode string “漢字”. An EmailMessage object is created with a subject, an empty body, a from address, and a to address, and its encoding is set to ISO-8859-1. When the message is generated, the test asserts that the Message-ID header contains the punycode equivalent (“xn--p8s937b”) of the patched DNS_NAME.

Runtime error
When the message object is constructed under these conditions, a Unicode encoding error occurs because the header value contains characters outside the ISO-8859-1 range. The failure happens while setting the Message-ID header, as the code tries to enforce single-line headers and encode them with the specified charset, leading to a UnicodeEncodeError for characters that cannot be encoded in Latin-1.