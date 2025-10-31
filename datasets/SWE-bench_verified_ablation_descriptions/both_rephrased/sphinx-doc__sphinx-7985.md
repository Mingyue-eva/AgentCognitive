linkcheck could also check local (internal) links  
Subject: linkcheck currently doesn't check local (internal) links, but this would be useful.

<!--
  Important: This is a list of issues for Sphinx, not a forum.
  If you'd like to post a question, please move to sphinx-users group.
  https://groups.google.com/forum/#!forum/sphinx-users

  Thanks,
-->

### Problem
See above.

#### Procedure to reproduce the problem
First, generate a new Sphinx project with sphinx-quickstart. In the main index.rst file, add two link references: one that points to an invalid external URL and another that points to a missing internal target. Then run the link checking process by invoking `make linkcheck`.

#### Error logs / results
During the linkcheck run, Sphinx tries to validate both the external and internal references. The external link check fails because the hostname cannot be resolved after multiple retries, causing the linkcheck builder to report an error and terminate with a non-zero exit status.

#### Expected results
Also a check for the local link.

### Reproducible project / your project
N/A

### Environment info
- OS: Arch Linux
- Python version: 3.6
- Sphinx version: 1.7.6