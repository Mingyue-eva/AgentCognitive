Q object __or__ appears to get all dunder related’s default columns and queryset raises ProgrammingError.  
Description  
There appears to be a difference in how Q object aliases are set up when OR’d. The get_default_columns for `agent__property_groups__id__in` only uses the primary key, whereas get_default_columns for `agent__property_groups__in` pulls in every field. That extra data in the subquery triggers a “subquery must return only one column” error.

Reproduction steps  
• Define a queryset on your model and annotate it with the count of related property groups:  
  `property_groups = PropertyGroup.objects.agent_groups(management_agent)`  
  `queryset = YourModel.objects.annotate(Count("agent__property_groups"))`  
• Apply a filter that OR’s two conditions: one checking membership in the full PropertyGroup queryset, the other checking for zero related groups:  
  `queryset.filter(Q(agent__property_groups__in=property_groups) | Q(agent__property_groups__count=0)).distinct()`  
• In Django 3.2 this produces a subquery that selects every field from `property_propertygroup` (id, created, updated, create_by, update_by, tenant_objs, name), causing the database to complain that the subselect returns multiple columns.  
• By contrast, if you replace the first condition with `agent__property_groups__id__in=property_groups.values_list("id", flat=True)` instead, only the id column is pulled into the alias, the subquery returns a single column, and the query succeeds.

Here is the error:

	return self.cursor.execute(sql, params)
 File "/venv/lib/python3.6/site-packages/django/db/utils.py", line 90, in __exit__
	raise dj_exc_value.with_traceback(traceback) from exc_value
 File "/venv/lib/python3.6/site-packages/django/db/backends/utils.py", line 84, in _execute
	return self.cursor.execute(sql, params)
django.db.utils.ProgrammingError: subquery must return only one column
LINE 1: ...ativemovingaverage"."id", T5."property_group_id", (SELECT U0...															 ^
