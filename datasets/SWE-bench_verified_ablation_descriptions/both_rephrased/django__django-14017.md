## Issue Description
Exists(...) & Q(...) works, but Q(...) & Exists(...) raise a TypeError

Reproduction  
If you combine an existence check on all products with an empty query using the AND operator, you get a valid combined filter that contains the existence clause followed by an empty AND grouping. However, if you reverse the order—applying the empty query first and then the existence check with the same AND operator—the operation fails instead of producing an equivalent filter.

Runtime error  
In that reversed case, the framework raises a type error when attempting to combine the two operands. It only accepts another query filter as the second operand and does not know how to handle an existence expression in that position, so it aborts with a type checking failure.

The & (and |) operators should be commutative on Q-Exists pairs, but it's not  
I think there's a missing definition of __rand__ somewhere.