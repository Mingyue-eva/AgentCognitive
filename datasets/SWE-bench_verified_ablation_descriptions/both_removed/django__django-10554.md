Union queryset with ordering breaks on ordering with derived querysets  
Description  
  (last modified by Sergei Maertens)  
May be related to #29692  

Evaluating the queryset instead of creating a new queryset makes the code proceed as expected.