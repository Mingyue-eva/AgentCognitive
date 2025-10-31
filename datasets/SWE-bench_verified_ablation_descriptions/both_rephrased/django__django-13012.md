## Issue Description
Constant expressions of an ExpressionWrapper object are incorrectly placed at the GROUP BY clause

Description

To reproduce this issue, call a function that takes a query expression, wraps it in an ExpressionWrapper with an integer output field, and then builds a Django ORM query that annotates that expression, groups by the computed value and another column, and aggregates a sum. If the expression you supply is just a constant (for example, the number three), the SQL that Django generates will include that constant in the GROUP BY clause alongside the other grouping column.

When you run that query against PostgreSQL, the database rejects it because aggregate functions (or literal expressions used in aggregation queries) are not allowed in the GROUP BY clause. The execution fails with a ProgrammingError at the moment the query is sent to the database.

Note that if you skip wrapping the constant in an ExpressionWrapper and instead annotate the value directly, Django correctly omits the constant from the GROUP BY clause and the query executes successfully.