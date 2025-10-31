Union queryset with ordering breaks on ordering with derived querysets  
Description  
    
    (last modified by Sergei Maertens)  
  
May be related to #29692  
  
To reproduce this issue, first retrieve all dimension IDs in a flat list. Then build a queryset by taking the dimensions with primary keys 10 and 11 and uniting them with the dimensions having primary keys 16 and 17, applying an ordering on the second set by the “order” field before the union. When you inspect this combined queryset, you see the expected four dimensions: boeksoort, grootboek, kenteken, and activa. Next, you clear any ordering on that queryset and ask for its list of primary keys; at that point you get [16, 11, 10, 17] as expected. However, if you then try to look at the original union queryset object again, it triggers an error instead of showing the same four instances.  
  
When you attempt to display the queryset a second time, the database returns a programming error indicating that an ORDER BY position is not in the select list. This happens during the representation or evaluation of the queryset after the orderings have been altered, and it prevents you from seeing the queryset contents.  
  
Evaluating the qs instead of creating a new qs makes the code proceed as expected.  
[dim.id for dim in qs]