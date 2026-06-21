Email messages crash on non-ASCII domain when email encoding is non-unicode.

Description

When the computer hostname is set in unicode (in my case "正宗"), and the email encoding is iso-8859-1, Python attempts to convert all headers to that encoding, including the Message-ID header. Django should be handling the encoding of the message properly.

Fix:
have django.core.mail.utils or django.core.mail.message convert domain name to punycode before using