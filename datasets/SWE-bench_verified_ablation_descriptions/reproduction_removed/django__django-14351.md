Q object OR appears to get all dunder-related default columns and queryset raises ProgrammingError.

There is a difference in how Q object aliases are set up when OR’d: using `agent__property_groups__id__in` only selects the ID column, but using `agent__property_groups__in` causes all fields to be added to the alias’s default columns. That leads to a “subquery must return only one column” error in Django 3.2 (it worked in 2.2.5).

Here is the error:

    return self.cursor.execute(sql, params)
  File "/venv/lib/python3.6/site-packages/django/db/utils.py", line 90, in __exit__
    raise dj_exc_value.with_traceback(traceback) from exc_value
  File "/venv/lib/python3.6/site-packages/django/db/backends/utils.py", line 84, in _execute
    return self.cursor.execute(sql, params)
django.db.utils.ProgrammingError: subquery must return only one column
LINE 1: ...ativemovingaverage"."id", T5."property_group_id", (SELECT U0...        ^