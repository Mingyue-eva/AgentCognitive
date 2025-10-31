## Issue Description  
Constant expressions of an ExpressionWrapper object are incorrectly placed at the GROUP BY clause  

Description  
I have a helper function, execQuery, that takes any Query expression, wraps it in an ExpressionWrapper with an IntegerField output, and then builds a queryset by annotating that wrapper as expr_res, selecting expr_res and column_a, and finally summing column_b. When I invoke this function with a constant expression—such as Value(3)—the SQL Django emits selects both column_a and the literal 3, and then groups by column_a and that literal. Postgres rejects this query and raises the following error:

django.db.utils.ProgrammingError: aggregate functions are not allowed in GROUP BY  
LINE 1: SELECT "model"."column_a", 3 AS "expr_res", SUM("model"."col...

By contrast, if I skip wrapping the constant and annotate directly with Value(3), Django omits the constant from the GROUP BY clause and the query runs without error.