5.1.2 ImportError while loading conftest (windows import folder casing issues)  
5.1.1 works fine. after upgrade to 5.1.2, the path was converted to lower case  

To reproduce the problem, uninstall pytest version 5.1.1, install version 5.1.2, and then invoke pytest in collection-only mode against the “PIsys” directory using the smoke marker. In this scenario, pytest unexpectedly lowercases the folder path, and it fails to locate and load the project’s conftest.py file. The expected outcome is that pytest preserves the original path casing and successfully discovers the configuration file.  

When pytest attempts to import the conftest module from the PIsys folder, it cannot resolve the module named “python” because the lowered path no longer matches the actual package structure. This manifests as a module-not-found error during test collection.