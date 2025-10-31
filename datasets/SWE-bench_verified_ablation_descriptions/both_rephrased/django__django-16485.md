floatformat() crashes on "0.00".

Description

Reproduction:
When you apply the floatformat filter to a value of zero expressed as the string "0.00" and request zero digits after the decimal point, you would expect it to return "0". The same behavior is seen if you pass a Decimal object representing 0.00 with a precision of zero.

Runtime error:
Instead of producing the formatted result, the function raises a ValueError stating that the requested precision is invalid because the minimum allowed precision is one.