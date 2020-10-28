## Get all tasks that are due today or prior to today
import asana

from asana_conky.helper import get_date_today, print_to_file
from asana_conky.configuration import Configuration
from asana_conky.task import Task


def main():
    config = Configuration()

    if not config.get('personal_access_token'):
        print("No value for PAT in your console environment")
        exit(1)

    # Construct an Asana client
    client = asana.Client.access_token(config.get('personal_access_token'))

    # Set things up to send the name of this script to us to show that you succeeded! This is optional.
    client.options['client_name'] = "asana_get_due_tasks"

    # Request data
    opt_fields = ['name', 'due_on', 'due_at']
    tasks = client.tasks.get_tasks_for_user_task_list(config.get('user_task_list_gid'), completed_since='now', opt_fields=opt_fields, opt_pretty=True)

    today = get_date_today()
    # Iterate over tasks, and store only the ones that are due
    due_tasks = []
    for task in tasks:
        if task['due_on'] is not None:
            if task['due_on'] <= today:
                due_tasks.append(Task(task['name'], task['due_on'], task['due_at']))

    # Sort tasks by due date
    # due_tasks = sorted(due_tasks, key=lambda dt: dt['due_at'] if dt['due_at'] else dt['due_on'])
    due_tasks = sorted(due_tasks)

    # Format
    lines = []
    for dt in due_tasks:
        if config.get('show_time') is False:
            lines.append("{} - {}".format(dt.due_date.strftime("%d.%m"), dt.name))
        elif dt.due_time is None:  # maybe we have to remove the '        ' if there no items do have due_at
            lines.append("{}         - {}".format(dt.due_date.strftime("%d.%m"), dt.name))
        else:
            lines.append("{} {} - {}".format(dt.due_date.strftime("%d.%m"), dt.due_time.strftime("%H:%M"), dt.name))

    print_to_file(config.get('output_file_path_due_tasks'), lines)


if __name__ == '__main__':
    main()
