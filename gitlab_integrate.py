import sublime, sublime_plugin
import os, sys, inspect

cmd_subfolder = os.path.realpath(os.path.abspath(os.path.join(os.path.split(inspect.getfile( inspect.currentframe() ))[0],"dependencies")))
if cmd_subfolder not in sys.path:
	sys.path.insert(0, cmd_subfolder)

import gitlab

#Functions with "Prompt" in the name generally display either the quick bar or the menu
#and accept user input (although in some cases they don't do anything with that input)

INTRO_TEXT_FILE = "intro_text.txt"

#Settings field names
SETTINGS_FILE = "GitlabIntegrate.sublime-settings"
HOST_SETTING = "gli_project_host"
ID_SETTING = "gli_project_id"
TOKEN_SETTING = "gli_user_token"
DISPLAY_INTRO_SETTING = "gli_display_intro"

#Settings default/unset values
NO_HOST = "host not set"
NO_TOKEN = "token not set"

#Errors
ERR_PREFIX = "ERROR: "
ERR_COULD_NOT_CONNECT = ERR_PREFIX + "Host or Token not set, could not connect to Gitlab"
ERR_NOT_CREATED = ERR_PREFIX + "issue not created"
ERR_NOT_EDITED = ERR_PREFIX + "issue not edited"
ERR_NOT_ASSIGNED = ERR_PREFIX + "issue not assigned"
ERR_NOT_LABELED = ERR_PREFIX + "label(s) not added"
def ERR_NOT_FOUND(item): return ERR_PREFIX + "issue {0} not found".format(item)

settings = sublime.load_settings(SETTINGS_FILE)
project_host=settings.get(HOST_SETTING, NO_HOST)
project_id=settings.get(ID_SETTING, 0) 
user_token= settings.get(TOKEN_SETTING, NO_TOKEN)

class GliToolbarMenuCommand(sublime_plugin.WindowCommand):
	def run(self, command):
		_check_settings()
		display_intro = settings.get(DISPLAY_INTRO_SETTING, True)

		if not display_intro:
			if command == "create_issue":
				self.window.run_command("gli_prompt_create_issue")
			elif command == "edit_issue":
				self.window.run_command("gli_prompt_edit_issue")
			elif command == "assign_issue":
				self.window.run_command("gli_prompt_assign_issue")
			elif command == "label_issue":
				self.window.run_command("gli_prompt_label_issue")
			elif command == "select_issue":
				self.window.run_command("gli_prompt_select_issue")
			elif command == "input_project":
				self.window.run_command("gli_prompt_input_project")
			elif command == "select_project":
				self.window.run_command("gli_prompt_select_project")
		else:
			self.show_intro()

class GliPromptGitlabCommand(sublime_plugin.WindowCommand):
	def run(self):
		_check_settings()

		display_intro = settings.get(DISPLAY_INTRO_SETTING, True)

		if not display_intro:
			ACTIONS = ["Create Issue", "Edit Issue", "Assign Issue", "Add Label(s) To Issue", 
			"Get Issues", "Input Project ID", "Select Project ID"]
			self.window.show_quick_panel(ACTIONS, self.on_done)
		else:
			self.show_intro()

	def show_intro(self):
		#Sublime 2 & 3
		intro_view = self.window.open_file(INTRO_TEXT_FILE)
		intro_view.set_scratch(True)
		intro_view.set_read_only(True)

		settings.set(DISPLAY_INTRO_SETTING, False)
		sublime.save_settings(SETTINGS_FILE)

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
			self.window.run_command("gli_prompt_select_issue")
		elif index == 5:
			self.window.run_command("gli_prompt_input_project")
		elif index == 6:
			self.window.run_command("gli_prompt_select_project")


class GliPromptCreateIssueCommand(sublime_plugin.WindowCommand):
	def run(self):
		self.window.show_input_panel("Create Issue (title, [desc], [assign_to], [\"labels_1, labels_2\"], [milestone]):", "", self.on_done, None, None)

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

		if not git.createissue(project_id, title=title, description=desc,
			assignee_id=assign_to, milestone_id=milestone, labels=labels):
			_status_print(ERR_NOT_CREATED)
			return False
		else:
			_status_print("new issue created")
			return True


class GliPromptEditIssueCommand(sublime_plugin.WindowCommand):
	def run(self):
		self.window.show_input_panel("Edit Issue (iid, [title], [desc], [assign_to], [state], [\"labels_1, labels_2\"], [milestone]):", "", self.on_done, None, None)

	def on_done(self, text):
		dict_keys = ["iid", "title", "desc", "assign_to", "state", "labels", "milestone"]
		arguments = _process_label_arguments(text)
		arg_dict = _process_keyword_arguments(arguments, dict_keys)

		sublime.run_command("gli_edit_issue", arg_dict)

#Edit an issue
class GliEditIssueCommand(sublime_plugin.ApplicationCommand):
	def run(self, iid, title="", desc="", assign_to="unused", state="", labels="", milestone=""):
		issue_id = _issue_iid_to_id(iid)
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
				_status_print(ERR_NOT_EDITED)
				return False
		
		if not git.editissue(project_id, issue_id, title=title, description=desc,
			assignee_id=assign_to, milestone_id=milestone, labels=labels, state_event=state):
			_status_print(ERR_NOT_EDITED)
			return False
		else:
			_status_print("issue edited")
			return True


class GliPromptAssignIssueCommand(sublime_plugin.WindowCommand):
	def run(self):
		self.window.show_input_panel("Assign Issue (iid, user):", "", self.on_done, None, None)

	def on_done(self, text):
		dict_keys = ["issue_iid", "assign_to"]
		arg_dict = _process_keyword_arguments(text, dict_keys)

		sublime.run_command("gli_assign_issue", arg_dict)
		
#Assign an issue someone	
class GliAssignIssueCommand(sublime_plugin.ApplicationCommand):
	def run(self, issue_iid, assign_to):
		issue_id = _issue_iid_to_id(issue_iid)

		if assign_to == "" or assign_to == " ": #if empty user specified, remove assignees
			git.editissue(project_id, issue_id, assignee_id=False)
			return True

		if not str(assign_to).isdigit():
			assign_to = _username_to_id(assign_to)

		if assign_to == False or (not git.editissue(project_id, issue_id, assignee_id=assign_to)):
			_status_print(ERR_NOT_ASSIGNED)		
			return False
		else:
			_status_print("issue assigned")
			return True


class GliPromptLabelIssueCommand(sublime_plugin.WindowCommand):
	def run(self):
		self.window.show_input_panel("Add Label(s) to Issue (iid, \"labels_1, labels_2\"):", "", self.on_done, None, None)

	def on_done(self, text):
		dict_keys = ["issue_iid", "labels"]
		arguments = _process_label_arguments(text)
		arg_dict = _process_keyword_arguments(arguments, dict_keys)

		sublime.run_command("gli_label_issue", arg_dict)

#Add labels to an issue without affecting the current labels
class GliLabelIssueCommand(sublime_plugin.ApplicationCommand):
	def run(self, issue_iid, labels):
		issue_id = _issue_iid_to_id(issue_iid)

		issue = git.getprojectissue(project_id, issue_id)

		issue["labels"].append(labels)
		labels = ", ".join(issue["labels"])
		
		if not git.editissue(project_id, issue_id, labels=labels):
			_status_print(ERR_NOT_LABELED)
			return False
		else:
			_status_print("labels added")
			return True

class GliPromptSelectIssue(sublime_plugin.WindowCommand):
	def run(self):
		full_proj_issues = _get_all_issues()

		open_issues = []
		closed_issues = []

		for issue in full_proj_issues:
			state = "-" + issue["state"][0].upper() #State flag: -O = open, -C = closed
			title = issue["title"]

			#Truncate long titles
			max_title_width = 39 #46 minus space for stateflag and iid
			if len(title) > max_title_width:
				title = title[:max_title_width]

			issue_string = "{iid:3}:{title:{title_width}} {state}".format(
				iid=issue["iid"], title=title, title_width=max_title_width, state=state)

			if state == "-O":
				open_issues.append(issue_string)
			elif state == "-C":
				closed_issues.append(issue_string)

		open_issues.sort(key=lambda issue: issue.split(":")[0])
		closed_issues.sort(key=lambda issue: issue.split(":")[0])

		full_proj_issues = open_issues + closed_issues

		for issue in full_proj_issues:
			print(issue)
		sublime.set_timeout(lambda: self.window.show_quick_panel(full_proj_issues,  self.on_done, sublime.MONOSPACE_FONT), 10)

	def on_done(self, index):
		#(Eventually) open a view to edit the issue
		pass

		
#Changes the project ID via input bar
class GliPromptInputProjectCommand(sublime_plugin.WindowCommand):
	def run(self):
		self.window.show_input_panel("New Project ID", "", self.on_done, None, None)

	def on_done(self, text):
		sublime.run_command("gli_change_project", {"proj_id":text})

#Displays all projects the user has access to with their IDs, allowing user to select which id to use
class GliPromptSelectProjectCommand(sublime_plugin.WindowCommand):
	projects_list = []
	def run(self):
		projects = git.getprojects()
		projects_list = []
		for proj in projects:
			projects_list.append(str(proj["name"]) + ": " + str(proj["id"]))
		
		projects_list.sort()		

		print("")
		for proj in projects_list:
			print(proj)

		#Timeout only needed for Sublime 3
		sublime.set_timeout(lambda: self.window.show_quick_panel(projects_list,  lambda index: self.on_done(index, projects_list)), 10)
		#self.window.show_quick_panel(projects_list, lambda index: self.on_done(index, projects_list)) #this works for ST2

	def on_done(self, index, projects_list):
		proj_id = projects_list[index].split(": ")[1]
		sublime.run_command("gli_change_project", {"proj_id":proj_id})


class GliChangeProjectCommand(sublime_plugin.ApplicationCommand):
	def run(self, proj_id):
		proj_id = int(proj_id.strip())
		global project_id
		project_id=proj_id

		_status_print("new project_id: " + str(proj_id))

		settings.set(ID_SETTING, proj_id)
		sublime.save_settings(SETTINGS_FILE)

######################## Various support functions
#Get an issue's ID from its IID (ID is an absolute value, IID is relative to a project)
def _issue_iid_to_id(iid):
	proj_issues = _get_all_issues()
	for issue in proj_issues:
		issue_iid = issue["iid"]
		if (int(iid) == int(issue_iid)):
			issue_id = issue["id"]
			return issue_id

	_status_print(ERR_NOT_FOUND(iid))
	return False

#Get a user's ID from their username
def _username_to_id(username):
	users=git.getusers()
	for user in users:
		this_username = user["username"]
		if this_username == username:
			user_id = user["id"]
			return user_id

	_status_print(ERR_NOT_FOUND(username))
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

#Update settings from file
def _check_settings():
	global settings
	settings = sublime.load_settings(SETTINGS_FILE)

	global project_host
	global project_id
	global user_token

	new_host=settings.get(HOST_SETTING, NO_HOST)
	new_id=settings.get(ID_SETTING, 0) 
	new_token= settings.get(TOKEN_SETTING, NO_TOKEN)

	#Reconnect to Gitlab if settings changed
	if new_host != project_host or new_token != user_token:
		if new_host == NO_HOST or new_token == NO_TOKEN:
			_status_print(ERR_COULD_NOT_CONNECT)
			settings.set(DISPLAY_INTRO_SETTING, True)
		else: 
			global git
			git = gitlab.Gitlab(new_host, token=new_token) #Connect with private token
			_status_print("Reconnected to Gitlab using host " + new_host + " and token " + new_token)

	project_host = new_host
	project_id = new_id
	user_token = new_token

	_status_print("project_id:" + str(project_id))

#Returns a list of all issues
def _get_all_issues():
	issues = []
	issues_page = git.getprojectissues(project_id, per_page=100)
	
	current_page = 1

	while issues_page:
		issues += issues_page
		current_page+=1
		issues_page = git.getprojectissues(project_id, page=current_page, per_page=100)
	
	return issues		

#Outputs a status bar message and a console message
def _status_print(message):
	message = "[GLI]:" + message
	print(message)
	sublime.status_message(message)