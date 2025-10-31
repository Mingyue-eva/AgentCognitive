## Issue Description
:type: and :rtype: gives false ambiguous class lookup warnings

**Describe the bug**
The implicit xrefs created by the info fields ``:type:`` and ``:rtype:`` seems to do lookup differently than explicit xref roles. For unqualified names it seems like they search for the name in every (sub)module instead of in the current module and then parent modules.

**To Reproduce**
We have two classes, both named A, defined in the modules `mod` and `mod.submod`. In our documentation we first reference them by their full paths (`mod.A` and `mod.submod.A`) in a function’s parameters and return types. Next, we switch the current module to `mod`, document another function using both unqualified `A` and qualified `mod.A` and `mod.submod.A`, and include the same parameters and return types. Finally, we set the current module to `mod.submod` and document a third function whose parameters and return types use `A`, `mod.A`, and `mod.submod.A`. When building the docs, each use of the unqualified `A` under `mod.submod` triggers warnings, and the parameter and return type marked with “BUG” end up resolving to `mod.A` instead of `mod.submod.A`.

The build emits:
```
index.rst:28: WARNING: more than one target found for cross-reference 'A': mod.A, mod.submod.A
index.rst:28: WARNING: more than one target found for cross-reference 'A': mod.A, mod.submod.A
index.rst:43: WARNING: more than one target found for cross-reference 'A': mod.A, mod.submod.A
index.rst:43: WARNING: more than one target found for cross-reference 'A': mod.A, mod.submod.A
```

**Expected behavior**
No warnings, and the two mentioned types should resolve to ``mod.submod.A``.

**Environment info**
- Sphinx version: tested both with v3.3 and with master