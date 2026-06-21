Case() crashes with ~Q(pk__in=[]).
Description

The following code generates a syntax error. 
User.objects.annotate(
    _a=Case(
        When(~Q(pk__in=[]), then=Value(True)),
        default=Value(False),
        output_field=BooleanField(),
    )
).order_by("-a").values("pk")

When this query runs, Django generates an ORDER BY clause with a CASE expression that has no condition before the THEN keyword, causing the database to raise a syntax error at “THEN.” 

I expected behavior to annotate all rows with the value True since they all match.
Relevant because ~Q(pk__in=[]) is a sentinel value that is sometimes returned by application code.