import sublime, sublime_plugin
import gitlab

settings = sublime.load_settings('GitlabIntegrate.sublime-settings')

PROJECT_HOST=settings.get("gli_project_host", " ")
PROJECT_ID=settings.get("gli_project_id", 0) #not fully constant; changed in PromptChangeProjectCommand()
USER_TOKEN= settings.get("gli_user_token", " ")#from /profile/account in GitLab

git = gitlab.Gitlab(PROJECT_HOST, token=USER_TOKEN) #Connect with private token

sublime.run_command("gli_startup_messages")
first_use = True

intro_text = """Thank you for installing GitlabIntegrate!

GitlabIntegrate functions can be accessed via the menu (Tools -> GitlabIntegrate) or with a keyboard shortcut (Ctrl+Shift+X (Windows/Linux), Cmd+Shift+X (Mac))

Before using GitlabIntegrate, you should configure the User Settings file. User settings can be found 3 ways (you may need to create the file if it doesn't exist):
	1. Via the menu at 
		Preferences -> Package Settings -> Gitlab Integrate -> Settings - User
	2. Via the menu at
		Tools -> Gitlab Integrate -> Access User Settings
	3. Via file browser at
		[sublime installation directory]/Packages/User/GitlabIntegrate.sublime-settings 

Then, copy and paste the following text into the file (replacing any text already there), editing the necessary fields:
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
}"""

class GliPromptGitlabCommand(sublime_plugin.WindowCommand):
	def run(self):
		global first_use
		if not first_use:
			actions = ["Create Issue", "Edit Issue", "Assign Issue", "Add Label(s) To Issue", 
			"Change Project ID", "Get Project IDs (console output)"]
			self.window.show_quick_panel(actions, self.on_done)
		else: 
			self.startup()
			first_use = False

	def on_done(self, index):
		if index == 0:
			self.window.run_command("gli_prompt_create_issue")
		elif index == 1:
			self.window.run_command("gli_prompt_edit_issue")
		elif index == 2:
			self.window.run_command("gli_prompt_assign_issue")
		elif index == 3:
			self.window.run_command("gli_prompt_label_issue")
		elif index == 4:
			self.window.run_command("gli_prompt_change_project")
		elif index == 5:
			self.window.run_command("gli_get_project_ids")

	def startup(self):
		print("\nLoaded settings:\nproject_host:" + PROJECT_HOST + "\nproject_id:" + str(PROJECT_ID) + "\nuser_token:" + USER_TOKEN)
		
		active_window = sublime.active_window()

		display_intro = settings.get("gli_display_intro", True)

		if display_intro:
			new_view = active_window.new_file()
			new_view.set_scratch(True)
			
			edit = new_view.begin_edit()
			new_view.insert(edit, 0, intro_text)
			new_view.end_edit(edit)

			settings.set("gli_display_intro", False)
			sublime.save_settings("GitlabIntegrate.sublime-settings")


class GliPromptCreateIssueCommand(sublime_plugin.WindowCommand):
	def run(self):
		self.window.show_input_panel("Create Issue (title, [desc], [assign_to], [\"labels_1, labels_2\"], [milestone]):", "", self.on_done, None, None)
		pass

	def on_done(self, text):
		dict_keys = ["title", "desc", "assign_to", "labels", "milestone"]
		arguments = _process_label_arguments(text)
		arg_dict = _process_keyword_arguments(arguments, dict_keys)

		sublime.run_command("gli_create_issue", arg_dict)

#Create an issue: does not allow for commas or double quotes in the description
class GliCreateIssueCommand(sublime_plugin.ApplicationCommand):
	def run(self, title, desc="", assign_to="", labels="", milestone=""):
		if not assign_to.isdigit() and len(assign_to.strip())>0:
			assign_to = _username_to_id(assign_to)

		if not git.createissue(PROJECT_ID, title=title, description=desc,
			assignee_id=assign_to, milestone_id=milestone, labels=labels):
			print("Error: issue not created")
			return False
		else:
			return True


class GliPromptEditIssueCommand(sublime_plugin.WindowCommand):
	def run(self):
		self.window.show_input_panel("Edit Issue (iid, [title], [desc], [assign_to], [state], [\"labels_1, labels_2\"], [milestone]):", "", self.on_done, None, None)
		pass

	def on_done(self, text):
		dict_keys = ["iid", "title", "desc", "assign_to", "state", "labels", "milestone"]
		arguments = _process_label_arguments(text)
		arg_dict = _process_keyword_arguments(arguments, dict_keys)

		sublime.run_command("gli_edit_issue", arg_dict)

#Edit an issue
class GliEditIssueCommand(sublime_plugin.ApplicationCommand):
	def run(self, iid, title="", desc="", assign_to="unused", state="", labels="", milestone=""):
		issue_id = _issue_iid_to_id(iid, PROJECT_ID)
		if state == "open": state="reopen"
		elif state == "closed": state="close"

		#Not sending an "assign_to" value leaves the assignees unchanged
		#Sending an "assign_to" value of "" erases the current assignees
		#Other values are evaluated and resolved to a user if (if possible)
		if assign_to == "unused":
			assign_to = ""
		elif assign_to=="":
			assign_to = False
		elif not str(assign_to).isdigit():
			assign_to = _username_to_id(assign_to)
			if assign_to == False:
				print("Error: issue not edited")
				return False
		
		if not git.editissue(PROJECT_ID, issue_id, title=title, description=desc,
			assignee_id=assign_to, milestone_id=milestone, labels=labels, state_event=state):
			print("Error: issue not edited")
			return False
		else:
			return True


class GliPromptAssignIssueCommand(sublime_plugin.WindowCommand):
	def run(self):
		self.window.show_input_panel("Assign Issue (iid, user):", "", self.on_done, None, None)
		pass

	def on_done(self, text):
		dict_keys = ["issue_iid", "assign_to"]
		arg_dict = _process_keyword_arguments(text, dict_keys)

		sublime.run_command("gli_assign_issue", arg_dict)
		
#Assign an issue someone	
class GliAssignIssueCommand(sublime_plugin.ApplicationCommand):
	def run(self, issue_iid, assign_to):
		issue_id = _issue_iid_to_id(issue_iid, PROJECT_ID)

		if assign_to == "" or assign_to == " ": #if empty user specified, remove assignees
			git.editissue(PROJECT_ID, issue_id, assignee_id=False)
			return True

		if not str(assign_to).isdigit():
			assign_to = _username_to_id(assign_to)

		if assign_to == False or (not git.editissue(PROJECT_ID, issue_id, assignee_id=assign_to)):
			print("Error: issue not assigned")
			return False
		else:
			return True


class GliPromptLabelIssueCommand(sublime_plugin.WindowCommand):
	def run(self):
		self.window.show_input_panel("Add Label(s) to Issue (iid, \"labels_1, labels_2\"):", "", self.on_done, None, None)
		pass

	def on_done(self, text):
		dict_keys = ["issue_iid", "labels"]
		arguments = _process_label_arguments(text)
		arg_dict = _process_keyword_arguments(arguments, dict_keys)

		sublime.run_command("gli_label_issue", arg_dict)

#Add labels to an issue without affecting the current labels
class GliLabelIssueCommand(sublime_plugin.ApplicationCommand):
	def run(self, issue_iid, labels):
		issue_id = _issue_iid_to_id(issue_iid, PROJECT_ID)

		issue = git.getprojectissue(PROJECT_ID, issue_id)

		issue["labels"].append(labels)
		labels = ", ".join(issue["labels"])
		
		if not git.editissue(PROJECT_ID, issue_id, labels=labels):
			print("Error: labels not edited")
			return False
		else:
			return True


#Changes the project ID
class GliPromptChangeProjectCommand(sublime_plugin.WindowCommand):
	def run(self):
		self.window.show_input_panel("New Project ID", "", self.on_done, None, None)
		pass

	def on_done(self, text):
		proj_id = int(text.strip())
		global PROJECT_ID
		PROJECT_ID=proj_id

		settings.set("gli_project_id", proj_id)
		sublime.save_settings("GitlabIntegrate.sublime-settings")

#Displays all projects the user has access to with their IDs
class GliGetProjectIdsCommand(sublime_plugin.WindowCommand):
	def run(self):
		projects = git.getprojects()
		projects_list = []
		for proj in projects:
			projects_list.append(str(proj["name"]) + ": " + str(proj["id"]))
		
		projects_list.sort()

		self.window.show_quick_panel(projects_list, self.on_done)

		print("")
		for proj in projects_list:
			print(proj)

	def on_done(self, index):
		pass

class GliStartupMessagesCommand(sublime_plugin.ApplicationCommand):
	def run(self):
		print("\nLoaded settings:\nproject_host:" + PROJECT_HOST + "\nproject_id:" + str(PROJECT_ID) + "\nuser_token:" + USER_TOKEN)
		
		active_window = sublime.active_window()

		display_intro = settings.get("gli_display_intro", True)

		if display_intro:
			new_view = active_window.new_file()
			new_view.set_scratch(True)
			
			edit = new_view.begin_edit()
			new_view.insert(edit, 0, intro_text)
			new_view.end_edit(edit)

			settings.set("gli_display_intro", False)
			sublime.save_settings("GitlabIntegrate.sublime-settings")


########################
#Get an issue's ID from its IID (ID is an absolute value, IID is relative to a project)
def _issue_iid_to_id(iid, proj_id=PROJECT_ID):
	proj_issues = git.getprojectissues(proj_id)
	for issue in proj_issues:
		issue_iid = issue["iid"]
		if (int(iid) == int(issue_iid)):
			issue_id = issue["id"]
			return issue_id

	print("Issue " + iid + " not found")
	return False

#Get a user's ID from their username
def _username_to_id(username):
	users=git.getusers()
	for user in users:
		this_username = user["username"]
		if this_username == username:
			user_id = user["id"]
			return user_id

	print("User " + username + " not found.")
	return False

#Handles keyword arguments, returns a dict of argname:value pairs
#	should be run after _process_label_arguments if labels are included
def _process_keyword_arguments(arguments, dict_keys):
	if not isinstance(arguments, list):
		arguments = arguments.split(",")

	arg_dict = {}
	nonkeyword_args = []
	keyword_not_encountered = True

	for arg in arguments:
		if "=" not in arg and keyword_not_encountered:
			nonkeyword_args.append(arg)
		else:
			arg = arg.split('=')
			arg_dict[arg[0].strip()]=arg[1]
			keyword_not_encountered = False

	if len(nonkeyword_args) > 0:
		for x in range(len(nonkeyword_args)):
			arg_dict[dict_keys[x]] = nonkeyword_args[x]

	for key in arg_dict.keys():
		if len(arg_dict[key]) > 1:
			arg_dict[key] = arg_dict[key].strip()

	return arg_dict

#Ensures labels are handled as one argument, returns a list of arguments
def _process_label_arguments(arguments):
	if not isinstance(arguments, list):
		arguments = arguments.split(",")

	label_end_indices = [] #indices of the first and last label
	for arg in arguments:
		for x in range(arg.count('"')):
			label_end_indices.append(arguments.index(arg))
	if len(label_end_indices) > 0:
		labels = ",".join(arguments[label_end_indices[0]:label_end_indices[1]+1]).replace('"','')
		arguments[label_end_indices[0]] = labels
		del arguments[label_end_indices[0]+1:label_end_indices[1]+1]

	return arguments