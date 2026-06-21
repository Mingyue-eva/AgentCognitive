Contains.as_set returns Contains

When you ask the system to convert the membership test “x is in the real numbers” into a set, it simply hands back the original membership test. In other words, calling as_set on Contains(x, Reals) returns Contains(x, Reals) instead of producing an actual set object.

This is wrong because Contains is not a set (it's a boolean). It results in failures in other places because it doesn't have as_relational (since it isn't a set). For instance, from https://github.com/sympy/sympy/pull/14965#discussion_r205281989

If you build a piecewise expression that returns 6 when x lies in the real numbers and 7 otherwise, the implementation tries to convert that membership test into a set and then into a relational expression. At runtime this fails with an attribute error, because the membership test object does not implement the required as_relational method.