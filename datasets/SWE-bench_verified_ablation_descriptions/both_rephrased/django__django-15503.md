has_key, has_keys, and has_any_keys JSONField() lookups don't handle numeric keys on SQLite, MySQL, and Oracle.

Description

(last modified by TheTerrasque)

Problem

When using models.JSONField() has_key lookup with numerical keys on a SQLite database, it fails to find entries whose JSON objects use numeric strings as keys.

Versions:
Django: 4.0.3  
Python: 3.9.6 on win32  
sqlite3.version: 2.6.0  
sqlite3.sqlite_version: 3.35.5  

Reproduction

Use a SQLite database and define a model with a JSONField. Create two records: one whose JSON data has a key named "foo" and another whose JSON data has a key named "1111", each with some value. Then perform two filtered queries—one asking for entries where the JSONField has the key "foo" and another where it has the key "1111". You expect each query to return exactly one matching record.

Expected Result

Both queries should report a count of one matching record.

Runtime Error

When running the test case, the lookup for the key "foo" succeeded and returned one record, but the lookup for the numeric key "1111" returned zero records. The test framework asserted that it should have found one entry with that key, and this assertion failed, indicating that the numeric key lookup did not work on SQLite.

Additional info

This has been tested on SQLite and PostgreSQL backends: it works on PostgreSQL but fails on SQLite.