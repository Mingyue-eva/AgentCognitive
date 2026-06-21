_check_homomorphism is broken on PermutationGroups

To reproduce the problem, load Sympy’s combinatorics package and build the dihedral group of order six. Then attempt to define a homomorphism from that group back to itself by sending each of its generators to itself. You would expect this to succeed and yield the identity homomorphism.

Instead, when you perform this mapping, the system raises a ValueError stating that “the given images do not define a homomorphism,” even though the images match the original generators exactly.

The issue is in the internal `_image()` function, where it handles the case of a `PermutationGroup`:

https://github.com/sympy/sympy/blob/809c53c077485ca48a206cee78340389cb83b7f1/sympy/combinatorics/homomorphisms.py#L336-L337

When `r[i]` is an inverted generator, the `in gens` test fails.

I think the whole thing can be greatly simplified.