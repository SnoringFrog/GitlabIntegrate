Sublime Gitlab Integration changelog
====================================

Version 1.2 - 8/20
------------------------------------
-`Change Project ID` renamed `Input Project ID`

-`Get Project IDs` replaced with `Select Project ID`

  -`Select Project ID functions identically to Get Project IDs` but changes the current project ID if a project is selected from the list

-`Get Issues` added

  -Displays a list of all issues (open and closed) in the current project, sorted by state and then by giiid

Version 1.1 - 8/19
------------------------------------
-GLI now runs on Sublime 3.

-intro_text.txt added

-error/success messages all appear in status bar (error are also in the console)

-settings are checked on most commands now

-various internal changes, mostly to make things work in ST3

Version 1.0 - 8/18
------------------------------------
-Initial release. 

-Supported features:

  -Get project IDs

  -Create Issues

  -Edit Issues

  -Quick functions for adding labels or assigning users to an issue
  
  -Issues can be assigned to users by the user ID or username
