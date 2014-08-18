This is a Sublime Text 2 Plugin that integrates various Gitlab features into the editor. 

Installation
----------
There are two ways to install.

1. If you have Package Control installed, create a .zip of the GitlabIntegrate folder in this directory and change its extension to `.sublime-package`. Place that file in `[your Sublime installation directory]/Installed Packages` and restart Sublime

2. Copy the GitlabIntegrate folder to `[your Sublime installation directory]/Packages/`


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

```
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