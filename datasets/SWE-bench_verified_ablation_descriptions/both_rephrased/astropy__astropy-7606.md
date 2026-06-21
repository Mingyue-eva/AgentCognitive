Unit equality comparison with None raises TypeError for UnrecognizedUnit

Reproduction
To trigger this problem, one creates a Unit instance using an unrecognized unit identifier with silent parsing enabled and then checks equality between that unit and None. The expected behavior is for the comparison to return False.

Runtime error
Rather than returning False, the comparison raises a type error during the equality check, because the code attempts to interpret None as a unit and rejects it as invalid.