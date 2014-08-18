This is a Sublime Text 2 Plugin that integrates various Gitlab features into the editor. To install, copy the GitlabIntegrate folder to `[your Sublime installation directory]/Packages/`

GitlabIntegrate functions can be accessed via the menu (`Tools -> GitlabIntegrate`) or with a keyboard shortcut (`Ctrl+Shift+X` (Windows/Linux), `Cmd+Shift+X` (Mac))

Before using GitlabIntegrate, you should configure the User Settings file. User settings can be found 3 ways (you may need to create the file if it doesn't exist):

1. Via the menu at 
   Preferences -> Package Settings -> Gitlab Integrate -> Settings - User
2. Via the menu at
   Tools -> Gitlab Integrate -> Access User Settings
3. Via file browser at
   [sublime installation directory]/Packages/User/GitlabIntegrate.sublime-settings 


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
