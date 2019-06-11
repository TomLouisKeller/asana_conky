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

# Sort the tasks in the list by due_date
def sort_tasks_by_due_date(tasks):

    logger.debug(json.dumps(tasks, sort_keys=False, indent=2))

    return tasks


# Create label from task
# Format: #date# - #parent_name# -> #name#
def get_task_label(gid):
    task = get_task(gid)['data']
    
    task_label=""
    
    task_label += task['due_on']

    task_label += " -> "

    # TODO: Could do this recursive (parent of parent etc. get parent's gid and get the task, see if it has a parent)
    if task['parent'] is not None:
        task_label+=task['parent']['name']
        task_label+=" -> "

    task_label+=task['name']
    #logger.debug("DueToday: {} - {}".format(task['gid'], task['name']))
    #logger.debug(get_task(task['gid']))
    #logger.debug()
    return task_label

#def get_parent_task(gid):
#    pass

def print_to_file(content: list):
    file = open(output_file_path,"w") 
    for line in content:
        file.write(line + "\n")
    file.close() 

# Here the magic happens
def main():
    tasks = get_users_tasks()
    tasks = tasks['data']
    #tasks = tasks[0:30]

    # Remove all tasks that aren't due today or prior to that
    tasks = filter_due_tasks(tasks)

    # Sort by due date
    tasks = sort_tasks_by_due_date(tasks)

    logger.debug()
    logger.debug("Due today tasks:")
    task_labels = list()
    for task in tasks:
        task_labels.append(get_task_label(task['gid']))
    
    print_to_file(task_labels)

    logger.debug('Done')

main()
