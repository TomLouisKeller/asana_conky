# Here we get all the tasks with tags
# Here is how we do it: https://asana.com/developers/api-reference/tasks#query
# GET    /tags/{tag_gid}/tasks
# Need to figure out the tag id first: GET    /tags
# GET    /tags

import asana
from datetime import datetime
from helper import print_to_file
from configuration import Configuration


# any sane programming language would have a much easier way to do this, but here we are
# admitted, asana is also a cripple with its due_on and due_at rather than just storing a date and a time
class Task:

    def __init__(self, name: str, due_on: str, due_at: str):
        self.name = name

        if due_at is not None:  # remove the Z at the end of the iso string
            due_at = due_at[:-1]

        self.due_date = None
        self.due_time = None

        if due_on is not None and due_at is not None:
            if datetime.fromisoformat(due_on).strftime("%y-%d-%m") != datetime.fromisoformat(due_at).strftime("%y-%d-%m"):
                raise("due_on and due_at are not on the same date! what now?")
            else:
                self.due_date = datetime.fromisoformat(due_at).date()
                self.due_time = datetime.fromisoformat(due_at).time()
        elif due_on is not None:
            self.due_date = datetime.fromisoformat(due_on).date()
        elif due_at is not None:
            self.due_date = datetime.fromisoformat(due_at).date()
            self.due_time = datetime.fromisoformat(due_at).time()

    def __lt__(self, other):
        if self.due_time is not None and other.due_time is not None:
            return self.due_time < other.due_time
        elif self.due_date is not None and other.due_date is not None:
            if self.due_date == other.due_date:
                if self.due_time is not None:
                    return True
                else:
                    return False
            else:
                return self.due_date < other.due_date
        elif self.due_date is not None or self.due_time is not None:
            return True
        elif other.due_date is not None or other.due_time is not None:
            return False
        else:
            return self.name < other.name


def extract_tasks_from_tag(tag, client):
    # tasks = client.tasks.get_tasks_for_tag(config.get('user_task_list_gid'), completed_since='now', opt_fields=opt_fields, opt_pretty=True)
    opt_fields = ['name', 'due_on', 'due_at']
    api_tasks = client.tasks.get_tasks_for_tag(tag['gid'], completed_since='now', opt_fields=opt_fields, opt_pretty=True)

    # Add all tasks to a list, so we can sort it
    tasks = []
    for task in api_tasks:
        tasks.append(Task(task['name'], task['due_on'], task['due_at']))

    tasks = sorted(tasks)

    # Format
    lines = list()
    lines.append("# {}".format(tag['name']))
    for task in tasks:
        lines.append(task.name)
    return lines


def by_tag_label():
    config = Configuration()

    # Construct an Asana client
    client = asana.Client.access_token(config.get('personal_access_token'))

    # Set things up to send the name of this script to us to show that you succeeded! This is optional.
    client.options['client_name'] = "asana_tasks_by_tag_name"

    req_tags = client.tags.get_tags({'workspace': config.get('workspace_gid')}, opt_fields=['name'], opt_pretty=True)

    # Add all tags to a list, so we can sort it
    tags = dict()
    for req_tag in req_tags:
        tags[req_tag['name']] = req_tag

    lines = list()
    is_first = True
    for config_tag_name in config.get('tag-names'):
        if config_tag_name in tags.keys():
            if is_first:
                is_first = False
            else:
                lines.append("")
            lines.extend(extract_tasks_from_tag(tags[config_tag_name], client))

    [print(line) for line in lines]

    print_to_file(config.get('output_file_path_tags'), lines)


def by_tag_id():
    config = Configuration()

    # Construct an Asana client
    client = asana.Client.access_token(config.get('personal_access_token'))

    # Set things up to send the name of this script to us to show that you succeeded! This is optional.
    client.options['client_name'] = "asana_tasks_by_tag_id"

    is_first = True
    lines = list()
    for tag_id in config.get('tag-ids'):
        tag = client.tags.get_tag(tag_id, opt_fields=['name'], opt_pretty=True)

        if is_first:
            is_first = False
        else:
            lines.append("")

        lines.extend(extract_tasks_from_tag(tag, client))

    # [print(line) for line in lines]

    print_to_file(config.get('output_file_path_tags'), lines)


# by_tag_label()
by_tag_id()
