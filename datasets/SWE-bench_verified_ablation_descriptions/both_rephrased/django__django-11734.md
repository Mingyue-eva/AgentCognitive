OuterRef in exclude() or ~Q() uses wrong model.

Description

To reproduce the issue, a test is added in tests/queries/test_qs_combinators that works in two stages. First, the Number model is annotated with a boolean flag that uses an Exists subquery: it checks whether there is at least one Item whose associated tag’s category ID matches the Number record’s primary key. Applying a filter on this annotation to include only Number records for which the flag is true succeeds as expected.

Next, the same annotation is applied but the subquery is inverted – Item records with matching tag category are excluded instead of included – and the test filters again for records where the flag is true. An alternative variation negates the filter condition using a Q expression inside the Exists annotation. In both cases, however, the query does not complete. The expected outcome is that the query would simply return all Number records for which no Item has a tag category matching the Number primary key.

At runtime, attempting to run either the exclude-based or the negated-Q version of the annotation causes a ValueError to be raised. The error indicates that the queryset refers to an outer query and may only be used as part of a subquery, which prevents the test from completing successfully.