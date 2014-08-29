Sublime Gitlab Integration changelog
====================================
Version 1.3.2 - 8/29
------------------------------------
- Added threading to Edit Issue calls

Version 1.3.1 - 8/27
------------------------------------
- Canceling the quick panel for `Edit Issue in Tab` and `Select Project ID` now does nothing (as it should) instead of selecting the last item in the list

Version 1.3 - 8/26
------------------------------------
- `Edit Issue In Tab` replaced `Get Issues`
  - Allows you to select an issue and edit it in a new tab. Close to send changes.

- Characters are now escaped with a backslash (`\`) instead of a forward slash (`/`)

Version 1.2.3 - 8/25
------------------------------------
- Fixed issues with output_prefix breaking GLI for Sublime 2

- Added documentation about commands and arguments to README.md

- Added a toolbar item for the main GLI prompt so that the keyboard shortcut would be displayed in the menu

Version 1.2.2 - 8/22
------------------------------------
- All settings except `display_intro` now check for values in .sublime-project files first

- `output_prefix` setting added (default value="[GLI]:"), all outputs now prefixed

- All commands now available in the Command Palette

  - Command Palette commands all begin with "GLI:"

Version 1.2.1 - 8/22
------------------------------------
- Overhaul of the settings system; renamed all settings. _This means if you're upgrading from a pre-1.2.1 version your user settings file will no longer work_

- Introduced ability to hide closed issues from `get_issues`

- Fixed reoccuring bug with settings not being loaded on startup.

- Commas, equals signs, and double quotes can now be included in fields if escaped with /

- `Select Project ID` now supports listing all projects, regardless of how many there are (previous limit was 20)

Version 1.2 - 8/20
------------------------------------
- `Change Project ID` renamed `Input Project ID`

- `Get Project IDs` replaced with `Select Project ID`

  - `Select Project ID` functions identically to `Get Project IDs` but changes the current project ID if a project is selected from the list

- `Get Issues` added

  - Displays a list of all issues (open and closed) in the current project, sorted by state and then by iid

Version 1.1 - 8/19
------------------------------------
- GLI now runs on Sublime 3.

- intro_text.txt added

- error/success messages all appear in status bar (error are also in the console)

- settings are checked on most commands now

- various internal changes, mostly to make things work in ST3

Version 1.0 - 8/18
------------------------------------
- Initial release. 

- Supported features:

  - Get project IDs

  - Create Issues

  - Edit Issues

  - Quick functions for adding labels or assigning users to an issue
  
  - Issues can be assigned to users by the user ID or username
