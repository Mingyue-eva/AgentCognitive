`is_subset` gives wrong results  
@sylee957 Current status on `master`,  
```python
>>> a = FiniteSet(1, 2)
>>> b = ProductSet(a, a)
>>> c = FiniteSet((1, 1), (1, 2), (2, 1), (2, 2))
>>> b.intersection(c) == c.intersection(b)
True
>>> b.is_subset(c)
>>> c.is_subset(b)
True
>>> Eq(b, c).simplify()
```
When simplifying the equality, an AttributeError is raised because a `Complement` object does not have an `equals` method.  
```python
>>> b.rewrite(FiniteSet)
      2
{1, 2}
>>> 
```