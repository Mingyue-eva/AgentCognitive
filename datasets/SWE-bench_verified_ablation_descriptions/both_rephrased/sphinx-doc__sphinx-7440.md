glossary duplicate term with a different case

**Describe the bug**  
When the documentation is built, the process reports that the term “mysql” appears more than once in the glossary. This duplicate entry is treated as an error, so the build fails.

**To Reproduce**  
If you clone the phpMyAdmin repository and then enter the documentation folder, install Sphinx, and trigger the HTML build, the build will halt because it encounters the duplicate “mysql” glossary entry.

**Expected behavior**  
MySQL != mysql term right ?

**Your project**  
https://github.com/phpmyadmin/phpmyadmin/blame/master/doc/glossary.rst#L234

**Environment info**  
- OS: Unix  
- Python version: 3.6  
- Sphinx version: 3.0.0

**Additional context**  
Did occur some hours ago, maybe you just released the version  
https://travis-ci.org/github/williamdes/phpmyadmintest/jobs/671352365#L328