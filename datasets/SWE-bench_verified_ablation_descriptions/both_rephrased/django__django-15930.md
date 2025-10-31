Case() crashes with ~Q(pk__in=[]).

Description

Reproduction
To reproduce this issue, build a Django query that retrieves User records, then add an annotation using a Case expression. In this Case, test whether the primary key does not appear in an empty list and return True if it does, otherwise return False. Next, order the results by this annotation in descending order and select only the primary key field. You should see every record marked as True in the annotation since none of the primary keys are in the empty list.

Runtime error
When this query runs, the database rejects the generated SQL because the conditional expression is malformed. The WHEN clause is empty, resulting in a fragment like “CASE WHEN THEN true ELSE false END,” which triggers a syntax error at the point where the condition was expected.

Relevant because ~Q(pkin=[]) is a sentinel value that is sometimes returned by application code.