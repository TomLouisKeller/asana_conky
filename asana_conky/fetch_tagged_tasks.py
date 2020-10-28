# Here we get all the tasks with tags
# Here is how we do it: https://asana.com/developers/api-reference/tasks#query
# GET    /tags/{tag_gid}/tasks
# Need to figure out the tag id first: GET    /tags
# GET    /tags

import asana
import re

from helper import print_to_file
from configuration import Configuration
from task import Task


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


def replace_text(file_path, start_tag, end_tag, lines):

    if file_path is None or start_tag is None or end_tag is None:
        print("Will not replace anything since file_path, start_tag or end_tag have not been provided")
        return

    # Read in the file
    with open(file_path, 'r') as file:
        filedata = file.read()

    print(f"filedata {filedata}")

    pattern = start_tag + ".*" + end_tag
    print(f"Pattern {pattern}")
    # regex = re.compile(r"^.*interfaceOpDataFile.*$", flags=re.MULTILINE)
    # regex = re.compile(pattern, flags=re.MULTILINE)
    regex = pattern
    print(f"regex {regex}")

    replaced = re.sub(regex, lines, filedata, flags=re.MULTILINE)

    print(f"replaced {replaced}")
    
    #Write the file out again
    with open(file_path, 'w') as file:
        file.write(replaced)


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

    line_string = ""
    for line in lines:
        line_string += line + "\n"

    # print_to_file(config.get('tagged_tasks')['output_path'], lines)
    replace_text(config.get('tagged_tasks')['output_path'], config.get('tagged_tasks')['start_tag'], config.get('tagged_tasks')['end_tag'], line_string)


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

    line_string = ""
    for line in lines:
        line_string += line + "\n"

    # print_to_file(config.get('tagged_tasks')['output_path'], lines)
    replace_text(config.get('tagged_tasks')['output_path'], config.get('tagged_tasks')['start_tag'], config.get('tagged_tasks')['end_tag'], line_string)


# by_tag_label()
by_tag_id()
