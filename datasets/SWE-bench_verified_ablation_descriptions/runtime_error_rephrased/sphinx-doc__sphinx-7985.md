Subject: linkcheck currently doesn't check local (internal) links, but this would be useful.

Problem  
See above.

Procedure to reproduce the problem  
Create a template project with sphinx-quickstart, put the following in index.rst  
```
broken external-link_
broken local-link_

.. _external-link: https://lkfqhlkghflkhs
.. _local-link: doesntexist
```
Run `make linkcheck`

Error logs / results  
When running `make linkcheck`, Sphinx reports that the local reference “doesntexist” cannot be resolved and that it failed to establish an HTTPS connection to https://lkfqhlkghflkhs because the host name could not be found after multiple retries. The build finishes with problems and make exits with status 1.

Expected results  
Also a check for the local link.