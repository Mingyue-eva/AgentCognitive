SelectDateWidget can crash with OverflowError.

The issue occurs during form validation in SelectDateWidget.value_from_datadict, where user-controlled year, month, and day values are passed directly to datetime.date without overflow checks. Supplying integers larger than sys.maxsize causes datetime.date to raise an OverflowError.