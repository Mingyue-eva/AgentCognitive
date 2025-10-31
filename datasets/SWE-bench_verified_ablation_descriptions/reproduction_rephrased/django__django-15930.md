Case() crashes with ~Q(pk__in=[]).  
Description  

A developer constructs a Django queryset that annotates each User with a boolean field named `_a`, using a Case expression that returns True when the user’s primary key is not in an empty list and False otherwise. The queryset is then ordered by this annotation in descending order, and only the `pk` values are retrieved.  

The error is:  
ProgrammingError: syntax error at or near "THEN"  
LINE 1: ..._user"."id" FROM "users_user" ORDER BY CASE WHEN THEN true ...  
The generated SQL is:  
SELECT "users_user"."id" FROM "users_user" ORDER BY CASE WHEN THEN True ELSE False END ASC  
I expected behavior to annotate all rows with the value True since they all match.  
Relevant because ~Q(pkin=[]) is a sentinel value that is sometimes returned by application code.