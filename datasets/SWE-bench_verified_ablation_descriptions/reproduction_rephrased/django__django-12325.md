pk setup for MTI to parent get confused by multiple OneToOne references.  
Description

In a minimal setup, you have a base Document model and then a Picking subclass that declares two OneToOneField links back to Document. If you list the parent‐link field first and the other reference second, Django raises  
django.core.exceptions.ImproperlyConfigured: Add parent_link=True to appname.Picking.origin.  
Strikingly, when you reverse that order—defining the origin field before the parent‐link field—the configuration succeeds without error.

First issue is that order seems to matter?  
Even if ordering is required "by design" (it shouldn’t be, since we have an explicit parent_link marker) shouldn’t it be processed in the order it appears, like managers and other class attributes?