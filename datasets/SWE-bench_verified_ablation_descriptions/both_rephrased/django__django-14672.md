Missing call `make_hashable` on `through_fields` in `ManyToManyRel`
Description

In 3.2 identity property has been added to all ForeignObjectRel to make it possible to compare them. A hash is derived from said identity and it's possible because identity is a tuple. To make limit_choices_to hashable (one of this tuple elements), ​there's a call to make_hashable.
It happens that through_fields can be a list. In such case, this make_hashable call is missing in ​ManyToManyRel.
For some reason it only fails on checking proxy model. I think proxy models have 29 checks and normal ones 24, hence the issue, but that's just a guess.

Minimal repro:
First, define a simple model called Parent with a character field, then create a ProxyParent model that inherits from Parent and is marked as a proxy. Next, add a Child model that includes a foreign key to Parent and sets up a many-to-many relationship back to Parent using an explicit through model. Specify the two through model fields by name and assign a related name. Then implement the through model with two required foreign keys linking to Parent and Child and an additional optional foreign key to Child. After these models are in place, run Django’s system checks or attempt to start the project. Under normal circumstances, the model definitions should pass validation without any errors.

Which will result in
When Django runs the model checks, it tries to include the through_fields list in the identity tuple used for hashing reverse relations. Because that list is not converted into a hashable form, the validation process fails with a TypeError complaining that a list is unhashable.

Solution: Add missing make_hashable call on self.through_fields in ManyToManyRel.

Missing call `make_hashable` on `through_fields` in `ManyToManyRel`
Description

In 3.2 identity property has been added to all ForeignObjectRel to make it possible to compare them. A hash is derived from said identity and it's possible because identity is a tuple. To make limit_choices_to hashable (one of this tuple elements), ​there's a call to make_hashable.
It happens that through_fields can be a list. In such case, this make_hashable call is missing in ​ManyToManyRel.
For some reason it only fails on checking proxy model. I think proxy models have 29 checks and normal ones 24, hence the issue, but that's just a guess.

Minimal repro:
Start by declaring a Parent model with a text field and then creating a ProxyParent model that extends it as a proxy. Introduce a Child model that holds a foreign key to Parent and establishes a many-to-many link back to Parent through a custom intermediary model, explicitly naming the two link fields in a list and assigning a related name. Finally, define the intermediary model with two mandatory foreign keys for Parent and Child plus an extra nullable foreign key to Child. Once these are defined, execute the Django management command that performs system checks. You would expect all field configurations to validate cleanly.

Which will result in
During the system check phase, Django attempts to hash the relation identity and encounters the through_fields list, which has not been converted to a hashable form. As a result, the check process raises a TypeError indicating that a list is unhashable.

Solution: Add missing make_hashable call on self.through_fields in ManyToManyRel.