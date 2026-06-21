Query.change_aliases raises an AssertionError

Description

Python Version: 3.9.2  
Django Version: 2.2.24, 3.2.9

I have encountered this bug while working on a project and reproduced it in a minimal setup. When performing an __or__ operation on two QuerySets, in Query.combine the aliases from the right-hand Query may collide with existing aliases in the left-hand Query. Calling Query.table_alias in Query.join then generates overlapping mappings (for example mapping T4→T5 and T5→T6), causing the AssertionError in change_aliases.

Expectation

Please fix this by ensuring new aliases do not intersect with existing ones—e.g. by passing rhs.alias_map into Query.join/Query.table_alias and incrementing suffixes until they’re unique. Also, document the assertion in change_aliases to explain that it prevents remapping an alias twice, and note in the docs that QuerySet OR is not commutative.