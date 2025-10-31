Using SimpleLazyObject with a nested subquery annotation fails.  
Description  
(last modified by Jordan Ephron)  

Prior to 35431298226165986ad07e91f9d3aca721ff38ec it was possible to use a SimpleLazyObject in a queryset as demonstrated below. This new behavior appears to be a regression.  

Sorry for the somewhat arbitrary testcase, hopefully it's sufficient to repro this issue.