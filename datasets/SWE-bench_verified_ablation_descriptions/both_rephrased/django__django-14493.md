ManifestStaticFilesStorage crashes with max_post_process_passes = 0.  
Description  

To reproduce:  
You create a custom storage class that inherits from ManifestStaticFilesStorage and override its max_post_process_passes setting to zero. You then point Django’s STATICFILES_STORAGE setting to this custom class and run the collectstatic management command. You would expect collectstatic to finish its post-processing step normally and output the processed files, but it never completes successfully.  

Runtime error:  
As soon as collectstatic begins using this configuration, it raises an UnboundLocalError because the code tries to reference a variable named substitutions before it has ever been initialized. This happens when the loop that assigns substitutions doesn’t run at all due to max_post_process_passes being zero.  

The error can also be seen easily in the code: ​https://github.com/django/django/blob/a0a5e0f4c83acdfc6eab69754e245354689c7185/django/contrib/staticfiles/storage.py#L246-L257  
substitutions is only set if the loop is entered at least once.  
(The motivation to set max_post_process_passes to 0 is to have Django not produce invalid CSS as described here: https://code.djangoproject.com/ticket/21080#comment:19 )