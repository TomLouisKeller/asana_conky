## Get all tasks that are due today or prior to today
import asana

from asana_conky.configuration import Configuration
from asana_conky.task import Task
from asana_conky.helper import get_date_today, replace_text_in_file, get_absolute_path
from asana_conky.asana_service import replace_task_in_string


def fetch_todays_tasks():
    config = Configuration()
    output_path = get_absolute_path(config.get('due_tasks')['output_path'])

    if not config.get('personal_access_token'):
        print("No value for PAT in your console environment")
        exit(1)

    # Construct an Asana client
    client = asana.Client.access_token(config.get('personal_access_token'))

    # Set things up to send the name of this script to us to show that you succeeded! This is optional.
    client.options['client_name'] = "asana_get_due_tasks"

    due_tasks = get_due_tasks(client, config)

    output_string = ""
    for task in due_tasks:
        output_string += replace_task_in_string(config.get('due_tasks')['task_format'], task, config)

    replace_text_in_file(output_path, config.get('due_tasks')['start_tag'], config.get('due_tasks')['end_tag'], output_string)


def get_due_tasks(client: asana.Client, config: Configuration):
    # Request data
    tasks = client.tasks.get_tasks_for_user_task_list(config.get('user_task_list_gid'), completed_since='now', opt_fields=['name', 'due_on', 'due_at'])

    today = get_date_today()
    # Iterate over tasks, and store only the ones that are due
    due_tasks = []
    for task in tasks:
        if task['due_on'] is not None:
            if task['due_on'] <= today:
                due_tasks.append(Task(task['gid'], task['name'], task['due_on'], task['due_at']))

    # Sort tasks by due date
    return sorted(due_tasks)


if __name__ == '__main__':
    fetch_todays_tasks()
