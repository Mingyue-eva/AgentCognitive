:type: and :rtype: gives false ambiguous class lookup warnings

**Describe the bug**  
The implicit xrefs created by the info fields ``:type:`` and ``:rtype:`` seem to do lookup differently than explicit xref roles. For unqualified names it seems like they search for the name in every (sub)module instead of in the current module and then parent modules.

**To Reproduce**  
First, define two classes with the same name in different modules: one in `mod.A` and another in `mod.submod.A`.  
Next, create a function in the top‐level module that uses both classes in explicit cross‐references and in parameter and return‐type annotations, mixing fully qualified names (`mod.A`, `mod.submod.A`) and unqualified names (`A`).  
Then switch the documentation context to the `mod` module and repeat a similar function, again annotating parameters and return types with unqualified `A` alongside `mod.A` and `mod.submod.A`.  
Finally, set the current module to `mod.submod` and document another function where you use unqualified `A` together with the two qualified references.  
When you build the docs with Sphinx, you will see warnings for each place you used the unqualified name.

**Observed behavior**  
During the build, Sphinx issues four warnings complaining that the cross‐reference “A” is ambiguous because it matches both `mod.A` and `mod.submod.A`.

**Expected behavior**  
No warnings, and the two unqualified references to `A` in the `mod.submod` context should resolve to `mod.submod.A`.

**Environment info**  
- Sphinx version: tested both with v3.3 and with master