## Get all tasks that are due today or prior to today
# Unfortunately the asana api doesn't let us query
# by due date or at least by assignee_status = inbox
# so we have to get all the tasks in the "My Tasks"
# list and then fetch one after another to get the due date
# and sort out the one's that have a due date prior to, 
# and including today

import requests
import json
from time import gmtime, strftime
from helper import get_logger
from configuration import Configuration

# Get configuration
config = Configuration()
personal_access_token = config.get('personal_access_token')
user_task_list_gid = config.get('user_task_list_gid')
output_file_path = config.get('output_file_path')

logger = get_logger()

headers = {'Authorization': 'Bearer {personal_access_token}'.format(personal_access_token=personal_access_token)}

# Get all tasks in the "My Tasks"-List
def get_users_tasks():
    url = "https://app.asana.com/api/1.0/user_task_lists/{user_task_list_gid}/tasks".format(user_task_list_gid=user_task_list_gid)
    params = {'completed_since': 'now'}
    response = requests.get(url, params=params, headers=headers)
    response_json = response.json()
    return response_json

# Remove all tasks that aren't due today or prior to that
def filter_due_tasks(tasks):
    today = get_date_today()
    due_tasks = list()
    for task in tasks:
        logger.debug("FromAllTasks: {} - {}".format(task['gid'], task['name']))
        due_on = get_due_on(task['gid'])
        if due_on is not None and due_on <= today:
            due_tasks.append(task)
    return due_tasks

# Get a Task based on it's gid
def get_task(gid):
    url = "https://app.asana.com/api/1.0/tasks/{gid}".format(gid=gid)
    response = requests.get(url, headers=headers)
    response_json = response.json()
    return response_json

# Get the due-on parameter of a task
def get_due_on(gid):
    data = get_task(gid)
    return data['data']['due_on']

# Return today's date
def get_date_today():
    return strftime("%Y-%m-%d", gmtime())

# Create label from task
# Format: #date# - #parent_name# -> #name#
def get_task_label(gid):
    task = get_task(gid)['data']
    
    task_label = task['due_on'] + " -> "

    # Recursively get the names of all parent tasks
    logger.debug('Get parent of task: {}'.format(task['name']))

    parents_name_string = get_parent_task(task['parent'])
    if parents_name_string is not "":
            parents_name_string += " - > "

    task_label += parents_name_string
    
    task_label += task['name']

    logger.debug("DueToday: {} - {}".format(task['gid'], task['name']))
    logger.debug(get_task(task['gid']))

    return task_label

def get_parent_task(parent):

    if parent is not None and 'gid' in parent and 'name' in parent:
        logger.debug("Parent gid: {} name: {}".format(parent['gid'], parent['name']))

        parent = get_task(parent['gid'])['data']
        parents_name_string = get_parent_task(parent['parent'])

        if parents_name_string is not "":
            parents_name_string += " - > "

        parents_name_string += parent['name']

        return parents_name_string
    else:
        return ""

# logger.debug(get_parent_task(dict({'gid':'1125180580548326', 'name':'Conky'})))


# Sort the tasks in the list by due_date
def sort_tasks_label(tasks):
    tasks.sort()
    return tasks

def print_to_file(content: list):
    file = open(output_file_path,"w") 
    for line in content:
        file.write(line + "\n")
    file.close() 

# Here the magic happens
def main():
    # Fetch all tasks from the "My Tasks" list
    tasks = get_users_tasks()
    tasks = tasks['data']

    # Remove all tasks that aren't due today or prior to that
    tasks = filter_due_tasks(tasks)

    # Create labels(simple text strings) from tasks
    logger.debug("Due today tasks:")
    task_labels = list()
    for task in tasks:
        logger.debug(task['name'])
        task_labels.append(get_task_label(task['gid']))
    
    # Sort tasks by due date
    task_labels = sort_tasks_label(task_labels)

    # Print labels to file
    print_to_file(task_labels)

    logger.debug('Done')

main()