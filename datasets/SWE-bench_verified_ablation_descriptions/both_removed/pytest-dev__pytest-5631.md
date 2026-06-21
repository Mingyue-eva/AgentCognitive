ValueError when collecting tests that patch an array

I’m trying to run pytest with a test file that contains a patch where “new” is an array. It works fine with pytest 3.1.3, but when using pytest 3.6.0 an error occurs upon collection.

Seems like a bug that was introduced by the following fix:
https://github.com/pytest-dev/pytest/commit/b6166dccb4d2b48173aa7e7739be52db9d2d56a0

When using @patch with new set to a NumPy array, p.new is an array and the check “p.new in sentinels” returns an array of booleans instead of a single boolean.