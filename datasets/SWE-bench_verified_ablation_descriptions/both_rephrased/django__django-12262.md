Custom template tags raise TemplateSyntaxError when keyword-only arguments with defaults are provided.  
Description  

(last modified by P-Seebauer)  

When defining a simple template tag that only accepts a single named argument with a default value, using that argument in a template triggers a template syntax error stating that the tag received an unexpected keyword argument. Likewise, if the argument has no default and is accidentally supplied twice, the error still indicates an unexpected keyword argument instead of reporting that the same argument was given multiple times. The same behavior is seen with inclusion tags. I already have a fix ready and will submit it after creating the corresponding ticket. This issue affects all versions since the problematic code was introduced in version 2.0.