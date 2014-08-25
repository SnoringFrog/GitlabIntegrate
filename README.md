Sublime Gitlab Integrate
========================
This is a Sublime Text 2 Plugin that integrates various Gitlab features into the editor. 

Installation
----------
There are three ways to install:

1. Clone this repository into `[your Sumblime installation directory]/Packages/`

2. Clone/download this repo wherever you'd like, then copy the files in it to `[your Sublime installation directory]/Packages/GitlabIntegrate`

3. If you have Package Control installed, create a `.zip` of the files in the repository (ignore any dotfiles) and change the `.zip` extension to `.sublime-package`. Place the `.sublime-package` in `[your Sublime installation directory]/Installed Packages/` and restart Sublime, Package Control should unpack it automatically.

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

**Command Arguments**: When entering a command, arguments must be comma-separated. All potential arguments are listed to the left of the input box within parentheses. Arguments in square brackets ([]) are optional. 

**Optional and Keyword Arguments**: Optional arguments may be specified as keyword arguments by prepending the argument value with its name and an unescaped equals sign (E.g., to create a new issue called "test_issue" and assign it to the user "robert" without specifying a description, you would type `test_issue, assign_to=username` into the `Create Issue` input box). If no keywords are specified, the arguments are processed left to right. 
With the exception of labels, every argument is represented by its keyword in the prompt.

**Special Notes on Arguments**:

- *Labels*: 
  -The keyword for labels is `labels`

  -If specifying more than one label, you must quote the whole list (e.g., for the `Add Label(s) to Issue` command for the issue with the iid 10, `10, "first_label, second_label" or `10, labels="first_label, second_label")

  -If you only specify one label, it does not matter if you quote it.

  -Specifying labels in the `Edit Issue` command will _replace all current labels_ . Explicitly specifying no labels (e.g. `labels=,`) will remove all labels from the issue.

- *Assign_to*: Users may be idenified by username or user_id (if you happen go know the id). GLI will automatically detect which method you've used.

- *Escaped Characters*: commas (,), equals signs (=), and double quotes (") in titles/descriptions must be escaped with a forward slash (/)