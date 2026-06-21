timesince() raises TypeError with USE_TZ=True and >1 month interval.
Description

(last modified by Sage Abdullah)

When you ask timesince() to report the difference for a datetime that was more than one month ago and you have USE_TZ set to True, it fails because it ends up trying to subtract a timezone-naive datetime from a timezone-aware one.

To reproduce the problem, turn on timezone support in Django and set USE_TZ to True. Then get the current time as a timezone-aware datetime, go back thirty-one days to create a past datetime, and call timesince on that value. Instead of seeing the expected text “1 month,” the call throws a TypeError about mixing naive and aware datetimes.

I believe this is happening because the pivot point created here: https://github.com/django/django/blob/d2310f6473593d28c14b63a72253408b568e100a/django/utils/timesince.py#L93-L100 does not carry over the original datetime’s tzinfo. Adding the tzinfo from the input datetime to that pivot call fixes the issue.

Happy to send a PR.