## Issue Description
floatformat() crashes on "0.00".  
Description

When you run Django’s floatformat filter on the literal '0.00' with a precision argument of 0—either by passing it as a string or as Decimal('0.00')—it raises the following error:

ValueError: valid range for prec is [1, MAX_PREC]