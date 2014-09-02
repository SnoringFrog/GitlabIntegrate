Adding new commands
-------------------
New commands should be referenced in the following files/functions:

- `Default.sublime-commands` - command palette entry

- `gitlab_integrate.py`:

  - `GliToolbarMenuCommand` - entry point for toolbar and command palette commands

    - `run()` - for prompt

    - `on_done()` - to trigger proper function

  - `GliPromptGitlabCommand.run()` - entry point from keyboard shortcut

- `Main.sublime-menu` - toolbar command list


Other notes
-----------
- Functions with "Prompt" in the name generally display either the quick bar or the menu and accept user input (although in some cases they don't do anything with that input)

- `_print()` is used for messages that go only to the console; `_status_print()` also goes to the status bar. Both are prefixed by `OUTPUT_PREFIX`

- `settings.reload_settings()` should be called at any plugin entry point

- `GliSelectIssueCommand()` and `EventDump()` are currently a messy nightmare of replacements. Changes to escape characters will likely break them.

- Submit pull requests, issues, or suggestions at [the Github repo](https://github.com/SnoringFrog/GitlabIntegrate) 