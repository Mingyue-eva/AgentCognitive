FieldError when migrating field to new model subclass.

Description

Analogous to #21890. If creating a model subclass and moving a field onto it in the same step, makemigrations works but migrate dies with django.core.exceptions.FieldError: Local field 'title' in class 'Book' clashes with field of the same name from base class 'Readable'.

Reproduction

Begin with a base model named Readable that defines a title field limited to 200 characters. Then refactor this so that Readable no longer defines title and introduce a new subclass called Book that declares its own title field. Run makemigrations, which generates operations to create the Book model with its title and to remove the title from Readable.

Expected result

The migration should apply cleanly, removing the title from the base class and adding it to the subclass without any conflict.

Runtime error

When running migrate, the process fails. Django raises a FieldError at the step where it tries to add title to Book, asserting that this field conflicts with the title field still present in the base class.

Reversing the order of the migration operations makes it pass. The auto-detector should be able to use this order.