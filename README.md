Sublime Gitlab Integrate
========================
This is a Sublime Text 2/3 Plugin that integrates various Gitlab features (primarily dealing with issue management, currently) into the editor. 

Installation
----------
There are 3 ways to install:

- With Package Control installed:
  1. (*Recommended*) Simply search for "Gitlab Integrate" in the "Install Package" menu and select it

- Without Package Control:
  1. Clone this repository into `[your Sumblime installation directory]/Packages/`
  2. Clone/download this repo wherever you'd like, then copy the files in it to `[your Sublime installation directory]/Packages/GitlabIntegrate`

Once installed, the plugin can be activated with `cmd+shift+x` (Mac) or `ctrl+shift+x` (Win/Linux).

Configuration
----------
Before using GitlabIntegrate, you should configure the User Settings file. If you do not, the introduction document will appear and prompt you to do so. User settings can be found 3 ways (you may need to create the file if it doesn't exist):

1. Via the menu at 

   `Preferences -> Package Settings -> Gitlab Integrate -> Settings - User`
2. Via the menu at

   `Tools -> Gitlab Integrate -> Access User Settings`
3. Via file browser at

   `[sublime installation directory]/Packages/User/GitlabIntegrate.sublime-settings` 

Then, copy and paste the following text into the file (replacing any text already there). Be sure to edit the project_host and user_token fields:

```javascript
{
	//The project host
	"project_host":"",

	//Your user token for GitLab, found in [host]/profile/account 
	"user_token":"",	

	//Displays the new installation window
	"display_intro":false,

	//The name of the tab when using Edit Issue In Tab (note: if you open another tab with this name, weird things might happen)
	"edit_issue_in_tab_name": "[GLI]: Editing Issue",

	//Suppresses output of closed issues for the Select Issue command
	"hide_closed_issues":false,

	//Appears before all GitlabIntegrate outputs in the console and status bar
	"output_prefix":"[GLI]:",

	/*
	The default project ID.
	This can be found by running GitlabIntegrate's "Get Project IDs" command after configuring 
	your host and user_token. All the projects you have access to should be listed with their IDs.
	*/
	"project_id": 0	
}
```

Usage
------
GitlabIntegrate functions can be accessed via the menu (`Tools -> GitlabIntegrate`), with a keyboard shortcut (`Ctrl+Shift+X` on Windows/Linux, `Cmd+Shift+X` on Mac), or via the Command Palette (default: `Cmd+Shift+P` on Mac, `Ctrl+Shift+P` on Windows/Linux). All GLI commands in the command palette begin with "GLI:".

**Edit Issue In Tab**: This mode opens the selected issue for editing in a separate view. To save your changes, simply close the tab.  

**Command Arguments**: When entering a command through the status/input bar, arguments must be comma-separated. All potential arguments are listed to the left of the input box within parentheses. Arguments in square brackets ([]) are optional. 

**Optional and Keyword Arguments**: Optional arguments may be specified as keyword arguments by prepending the argument value with its name and an unescaped equals sign (E.g., to create a new issue called "test_issue" and assign it to the user "robert" without specifying a description, you would type `test_issue, assign_to=username` into the `Create Issue` input box). If no keywords are specified, the arguments are processed left to right. 
With the exception of labels, every argument is represented by its keyword in the prompt.

**Special Notes on Arguments**:

- *Labels*: 

  - The keyword for labels is `labels`

  - If specifying more than one label, you must quote the whole list (e.g., for the `Add Label(s) to Issue` command for the issue #10 you would type: `10, "first_label, second_label"` or `10, labels="first_label, second_label"`)

  - If you only specify one label, it does not matter whether you quote it or not.

  - Specifying labels in the `Edit Issue` command will _replace all current labels_. Explicitly specifying no labels (e.g. `labels=,` or `labels="",`) will remove all labels from the issue.

- *Assign_to*: Users may be idenified by username or user_id (if you happen to know their id). GLI will automatically detect which method you've used.

- *Escaped Characters*: commas (`,`), equals signs (`=`), and double quotes (`"`) in titles/descriptions must be escaped with a backslash (`\`). Only double quotes must be escaped in the `Edit Issue In View` mode.

Modifying
---------
Before modifying GitlabIntegrate, users are encouraged to read [notes_for_modifying.md](./notes_for_modifying.md).
