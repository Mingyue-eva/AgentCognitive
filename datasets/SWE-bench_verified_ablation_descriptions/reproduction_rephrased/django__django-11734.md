OuterRef in exclude() or ~Q() uses wrong model.  
Description

I added a test to tests/queries/test_qs_combinators that annotates Number objects with an Exists subquery over Item. First, I check for Numbers that have at least one Item whose tags__category_id matches the Number’s primary key, and that works as expected. Then I change the subquery to exclude all Items with tags__category_id equal to the Number’s key—expecting to find Numbers with at least one non-matching Item—but evaluating the queryset crashes. Finally, I try to express the same exclusion via filter(~Q(tags__category_id=OuterRef('pk'))), and that also fails.

It results in the following error  
ValueError: This queryset contains a reference to an outer query and may only be used in a subquery