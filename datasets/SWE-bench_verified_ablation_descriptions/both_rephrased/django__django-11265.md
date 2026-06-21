Using exclude on annotated FilteredRelation doesn’t work

Description

It looks like using exclude on queryset with annotated FilteredRelation give a FieldError on the annotation name.

For example, in the Django test suite for filtered relations, there is a test that annotates the Author model with a relation called book_alice which only includes books whose title matches “poem by alice.” In the original test, applying a filter to include only those authors with a non-null book_alice annotation returns a single author as expected. If the test is changed to use exclude so that any author with a book_alice annotation is removed—thus expecting an empty result set—the query fails instead of returning no results. At the point where Django builds the exclusion clause, it raises an error saying that it cannot resolve the keyword book_alice into a field, listing only the model’s actual fields and relations. This indicates that the annotation defined earlier is not recognized when constructing the exclude filter.

As far as I understand, the function split_exclude(self, filter_expr, can_reuse, names_with_path) seams to be the faulty one. A new query is created without all extra datas from the original query.