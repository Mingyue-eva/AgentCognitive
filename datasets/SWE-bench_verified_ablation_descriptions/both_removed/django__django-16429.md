timesince() raises TypeError with USE_TZ=True and >1 month interval.

Description
(last modified by Sage Abdullah)

As of 8d67e16493c903adc9d049141028bc0fff43f8c8, calling timesince() with a datetime object that's one month or more in the past and USE_TZ=True fails due to a mismatch between offset-naive and offset-aware datetimes. The pivot datetime constructed in django/utils/timesince.py does not account for the input's tzinfo. Adding the input datetime’s tzinfo to the pivot call resolves the issue.

Happy to send a PR.