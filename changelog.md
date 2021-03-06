Sublime Gitlab Integration changelog
====================================
Version 1.5.1 - 6/22/15
------------------------------------
- Updated version number in metadata

Version 1.5.0 - 6/22/15
------------------------------------
- Updated included libraries, fixed plugin-breaking bug

Version 1.4.11 - 5/4/15 
------------------------------------
- Updated some outdated documentation

Version 1.4.10 - 10/22/14
------------------------------------
- Edited README for consistent display across Github/Gitlab/Package Control

Version 1.4.9 - 9/4/14
------------------------------------
- Typo fix for [messages.json](./messages.json)

Vertion 1.4.8 - 9/4/14
------------------------------------
- Added `.no-sublime-package`, should fix the current ST3 issues.

Version 1.4.7 - 9/4/14
------------------------------------
- Fixes ST3 "module not found"

Version 1.4.6b - 9/4/14
------------------------------------
- Beta of "module not found" fix for ST3

Version 1.4.5 - 9/3/14
------------------------------------
- Added keymap files to preferences menu

Version 1.4.4 - 9/3/14
------------------------------------
- Bugfixes for GLI in ST2, should work there now

- Changed `intro_text.txt` to [intro.txt](./messages/intro.txt)

- [intro.txt](./messages/intro.txt) is now loaded with a more reliable path

- Added `.sublime-workspace` to [.gitignore](./.gitignore)

Version 1.4.3 - 9/2/14
------------------------------------
- Added [messages.json](./messages.json) and set up messages directory

Version 1.4.2 - 9/2/14
------------------------------------
- Attempted Package Control installation fix (uneeded - issue turned out to be my impatience)

Version 1.4.1 - 9/2/14
------------------------------------
- Updated installation instructions

Version 1.4.0 - 9/2/14
------------------------------------
- Added `Toggle Issue State` command
  - Toggles an issue between open and closed

- Shortened `Hide Closed Issues in Get Issues` to `Hide Closed Issues` 

- Added [notes_for_modifying.md](./notes_for_modifying.md)

- Actually uploaded the [.sublime-commands](./Default.sublime-commands) file (should have been uploaded with v1.2.2). Command palette commands should work now

- GLI now available in Sublime Package Control

Version 1.3.2 - 8/29/14
------------------------------------
- Added threading to Edit Issue calls

Version 1.3.1 - 8/27/14
------------------------------------
- Canceling the quick panel for `Edit Issue in Tab` and `Select Project ID` now does nothing (as it should) instead of selecting the last item in the list

Version 1.3 - 8/26/14
------------------------------------
- `Edit Issue In Tab` replaced `Get Issues`
  - Allows you to select an issue and edit it in a new tab. Close to send changes

- Characters are now escaped with a backslash (`\`) instead of a forward slash (`/`)

Version 1.2.3 - 8/25/14
------------------------------------
- Fixed issues with output_prefix breaking GLI for Sublime 2

- Added documentation about commands and arguments to [the README](./README.md)

- Added a toolbar item for the main GLI prompt so that the keyboard shortcut would be displayed in the menu

Version 1.2.2 - 8/22/14
------------------------------------
- All settings except `display_intro` now check for values in `.sublime-project` files first

- `output_prefix` setting added (default value="[GLI]:"), all outputs now prefixed

- All commands now available in the Command Palette

  - Command Palette commands all begin with "GLI:"

Version 1.2.1 - 8/22/14
------------------------------------
- Overhaul of the settings system; renamed all settings. _This means if you're upgrading from a pre-1.2.1 version your user settings file will no longer work_

- Introduced ability to hide closed issues from `get_issues`

- Fixed reoccuring bug with settings not being loaded on startup.

- Commas, equals signs, and double quotes can now be included in fields if escaped with /

- `Select Project ID` now supports listing all projects, regardless of how many there are (previous limit was 20)

Version 1.2 - 8/20/14
------------------------------------
- `Change Project ID` renamed `Input Project ID`

- `Get Project IDs` replaced with `Select Project ID`

  - `Select Project ID` functions identically to `Get Project IDs` but changes the current project ID if a project is selected from the list

- `Get Issues` added

  - Displays a list of all issues (open and closed) in the current project, sorted by state and then by iid

Version 1.1 - 8/19/14
------------------------------------
- GLI now runs on Sublime 3.

- [intro_text.txt](./intro_text.txt) added

- error/success messages all appear in status bar (error are also in the console)

- settings are checked on most commands now

- various internal changes, mostly to make things work in ST3

Version 1.0 - 8/18/14
------------------------------------
- Initial release. 

- Supported features:

  - Get project IDs

  - Create Issues

  - Edit Issues

  - Quick functions for adding labels or assigning users to an issue
  
  - Issues can be assigned to users by the user ID or username
