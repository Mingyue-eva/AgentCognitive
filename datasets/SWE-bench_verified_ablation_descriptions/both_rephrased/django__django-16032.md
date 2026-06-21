__in doesn’t clear selected fields on the RHS when QuerySet.alias() is used after annotate()

Description

To reproduce the problem, first obtain all Book records whose page count exceeds 400. Then add an extra computed field to each book and give that field an alias. Next, find all Publisher records that have at least one book in this aliased, annotated set, and collect only their names. You should end up with exactly four publisher names: Apress, Sams, Prentice Hall, and Morgan Kaufmann.

When you run this sequence of operations, the database reports an operational error because the nested query returns ten columns when only one column is expected.