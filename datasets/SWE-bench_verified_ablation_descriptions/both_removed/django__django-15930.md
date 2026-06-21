Case() crashes when used with ~Q(pk__in=[]).  
This is relevant because ~Q(pk__in=[]) is a sentinel value that is sometimes returned by application code.