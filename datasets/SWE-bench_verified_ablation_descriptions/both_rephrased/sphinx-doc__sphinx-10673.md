## Issue Description
toctree contains reference to nonexisting document 'genindex', 'modindex', 'search'

**Is your feature request related to a problem? Please describe.**  
Many users want to include the automatically generated general index, module index, and search pages in their documentation sidebar. They configure a table of contents directive by setting a maximum depth of one, giving it the caption “Indices and tables,” and listing the page names genindex, modindex, and search. They expect those links to appear in the built documentation.

See:
* https://stackoverflow.com/questions/36235578/how-can-i-include-the-genindex-in-a-sphinx-toc
* https://stackoverflow.com/questions/25243482/how-to-add-sphinx-generated-index-to-the-sidebar-when-using-read-the-docs-theme
* https://stackoverflow.com/questions/40556423/how-can-i-link-the-generated-index-page-in-readthedocs-navigation-bar

However, when they build the HTML output, the build finishes but displays warnings stating that the documents 'genindex', 'modindex', and 'search' do not exist, so those entries are skipped in the table of contents.

**Describe the solution you'd like**  
The following directive should be possible and not produce any errors:
```
.. toctree::
   :maxdepth: 1
   :caption: Indices and tables

   genindex 
   modindex
   search
```