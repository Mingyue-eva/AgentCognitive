Management command subparsers don’t retain error formatting  
Description  
Django management commands use a subclass of argparse.ArgumentParser, CommandParser, that takes some extra arguments to improve error formatting. These arguments are not copied into subparsers, created via CommandParser.add_subparsers().add_parser(). Missing arguments to subparsers thus end as stack traces on the CLI, rather than human-facing usage messages.  

For example, imagine a custom management command that defines a subparser called “create” which requires a single positional argument for the item’s name.  
- If you run the command without specifying any subcommand, it prints the normal usage message and reports that the “create” subcommand is required.  
- If you invoke the “create” subcommand but omit the required name argument, instead of showing a concise error message, the command exits with a full Python traceback.  

In that failure case, a CommandError is raised inside the argument parser and the console displays the entire stack trace, ending with a note that the “name” argument is missing rather than presenting a simple usage reminder.  

We can correct this by ensuring that the subparser action returned by add_subparsers() copies the relevant arguments through to constructed subparsers.  

(Originally reported by Mark Gregson on django-developers: https://groups.google.com/g/django-developers/c/oWcaxkxQ-KI/m/4NUhLjddBwAJ)