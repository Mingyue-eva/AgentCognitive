floatformat() crashes on "0.00".
Description

from decimal import Decimal
from django.template.defaultfilters import floatformat
floatformat('0.00', 0)
floatformat(Decimal('0.00'), 0)
In both cases, Django raises a ValueError indicating that the precision parameter must be between 1 and MAX_PREC.