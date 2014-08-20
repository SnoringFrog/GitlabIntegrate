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

Then, copy and paste the following text into the file (replacing any text already there), editing the necessary fields:

```json
{
	//Displays the intro document on startup
	"gli_display_intro": false,

	//Your Gitlab host
	"gli_project_host": "",

	//Your Gitlab user token, found at [host]/profile/account 
	"gli_user_token": "",

	/*
	The default project ID.
	This can be found by running GitlabIntegrate's "Get Project IDs" command after configuring your host and user_token. All the projects you have access to should be listed with their IDs.
	*/
	"gli_project_id": 0
}
```

Usage
------
GitlabIntegrate functions can be accessed via the menu (`Tools -> GitlabIntegrate`) or with a keyboard shortcut (`Ctrl+Shift+X` (Windows/Linux), `Cmd+Shift+X` (Mac))
