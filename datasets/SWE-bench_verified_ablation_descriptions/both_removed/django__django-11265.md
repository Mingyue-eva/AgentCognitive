Using exclude on annotated FilteredRelation doesn't work

Description

It looks like using exclude on a queryset with an annotated FilteredRelation raises a FieldError on the annotation name.

As far as I understand, the function split_exclude(self, filter_expr, can_reuse, names_with_path) seems to be the faulty one. A new query is created without all extra data from the original query.