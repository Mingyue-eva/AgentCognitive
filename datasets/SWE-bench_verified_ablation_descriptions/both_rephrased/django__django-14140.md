Combining Q() objects with boolean expressions crashes.  
Description  
     
    (last modified by jonathan-golorry)  
     
Reproduction  
To reproduce the inconsistent behavior, import Q from django.db.models and construct a Q object with a single filter condition (for example, a field “x” equal to 1). When you invoke its deconstruct method, you will see that it reports no positional arguments and returns that single filter as a keyword argument. Next, create a Q object with two filter conditions (for example, “x” equals 1 and “y” equals 2) and call deconstruct again. In this case, you will observe that both conditions are returned together as positional arguments and no keyword arguments are reported. The expected result is that deconstruct should treat both single-condition and multi-condition Q objects in the same way.  

Runtime error  
When you use an Exists expression as the only child inside a Q object— for instance, wrapping a user lookup in Exists and passing that to Q— then call deconstruct, the operation fails. At the point where the code tries to unpack the single child into a key and a value, a TypeError occurs because the Exists object is not indexable.  

Patch https://github.com/django/django/pull/14126 removes the special case, meaning single-child Q objects deconstruct into args instead of kwargs. A more backward-compatible approach would be to keep the special case and explicitly check that the child is a length-2 tuple, but it's unlikely that anyone is relying on this undocumented behavior.