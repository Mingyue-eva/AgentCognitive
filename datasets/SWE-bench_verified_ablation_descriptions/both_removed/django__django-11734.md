OuterRef in exclude() or ~Q() uses wrong model.

Description

Using exclude() or ~Q() with OuterRef inside an Exists annotation causes the query to crash, whereas using filter() with OuterRef works as expected.