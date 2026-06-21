Result from clear_denoms() prints like the zero polynomial but behaves inconsistently due to an unstripped DMP. This inconsistency was the immediate cause of the ZeroDivisionError in #17990.

Calling clear_denoms on a complicated constant polynomial that is actually zero produces a Poly object that prints as zero yet reports is_zero=False in some contexts. Other Poly methods, such as terms_gcd, fail when applied to this “bad” polynomial. Although Poly.primitive has been improved recently to handle this case, earlier SymPy versions would raise a ZeroDivisionError.

The root cause is that the internal DMP representation retains a leading zero coefficient in its list, whereas the zero polynomial in the EX domain should have an empty coefficient list.