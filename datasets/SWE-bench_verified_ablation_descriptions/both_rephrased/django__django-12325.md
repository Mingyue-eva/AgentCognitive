pk setup for MTI to parent get confused by multiple OneToOne references.  
Description  

When you define a base model called Document and then create a subclass named Picking that includes two one-to-one relationships to Document—first marking document_ptr as the parent link and then defining an origin field without setting it as the parent link—Django raises an improper configuration error indicating that the second field also needs to be marked as the parent link. If you instead declare the origin field before document_ptr, Django processes the model definitions without any error.  

First issue is that order seems to matter?  
Even if ordering is required "by design" (it shouldn't be—we have an explicit parent_link marker) shouldn't it look from top to bottom like it does with managers and other things?