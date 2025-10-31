Micro-optimisation for Value._resolve_output_field (by modifying CharField.__init__)

Description

Currently, when you annotate(x=Value('test')), Value._resolve_output_field() ends up returning a CharField unconditionally for string values:

    if isinstance(self.value, str):
        return fields.CharField()

CharField.__init__ always adds a MaxLengthValidator even when max_length is None, which is extraneous in this context. Benchmarking shows that resolving the output field takes about 8.1 µs; removing the @deconstructible overhead brings it to about 6.96 µs; and avoiding the unnecessary validator instantiation reduces it further to about 5.86 µs—a roughly 2 µs improvement.

The proposed change is to mirror BinaryField.__init__ and only append the validator when max_length is set:

    if self.max_length is not None:
        self.validators.append(validators.MaxLengthValidator(self.max_length))

A local branch with this change passes all existing tests. It will be pushed to CI for further validation and broader testing.