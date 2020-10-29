# Here we get all the tasks with tags
# Here is how we do it: https://asana.com/developers/api-reference/tasks#query
# GET    /tags/{tag_gid}/tasks
# Need to figure out the tag id first: GET    /tags
# GET    /tags

import asana

from asana_conky.helper import replace_text_in_file  # , print_to_file
from asana_conky.configuration import Configuration
from asana_conky.task import Task


def extract_tasks_from_tag(tag, client):
    api_tasks = client.tasks.get_tasks_for_tag(tag['gid'], completed_since='now', opt_fields=['name', 'due_on', 'due_at'], opt_pretty=True)

    # Extract Tasks from API
    tasks = []
    for task in api_tasks:
        tasks.append(Task(task['name'], task['due_on'], task['due_at']))

    # Sort tasks
    tasks = sorted(tasks)

    # Format
    lines = list()
    lines.append("${goto 40}${font Bitstream Vera Sans:size=11}${color3}" + tag['name'] + "$color$font${voffset 2}")
    for task in tasks:
        lines.append("${goto 50}" + task.name)
    return lines


def by_tag_label():
    config = Configuration()

    # Construct an Asana client
    client = asana.Client.access_token(config.get('personal_access_token'))

    # Set things up to send the name of this script to us to show that you succeeded! This is optional.
    client.options['client_name'] = "asana_tasks_by_tag_name"

    # API call to get all tags of a certain workpsace
    req_tags = client.tags.get_tags({'workspace': config.get('workspace_gid')}, opt_fields=['name'], opt_pretty=True)

    # Extract Tags from API call
    tags = dict()
    for req_tag in req_tags:
        tags[req_tag['name']] = req_tag

    lines = list()
    lines.append('${voffset 8}\\')
    # Iterate over the tag names from config
    for config_tag_name in config.get('tag-names'):
        if config_tag_name in tags.keys():
            lines.extend(extract_tasks_from_tag(tags[config_tag_name], client))

    # for debug
    # [print(line) for line in lines]

    # Turn list of strings to string
    line_string = ""
    for line in lines:
        line_string += line + "\n"

    # print_to_file(config.get('tagged_tasks')['output_path'], lines)
    replace_text_in_file(config.get('tagged_tasks')['output_path'], config.get('tagged_tasks')['start_tag'], config.get('tagged_tasks')['end_tag'], line_string)


def by_tag_id():
    config = Configuration()

    # Construct an Asana client
    client = asana.Client.access_token(config.get('personal_access_token'))

    # Set things up to send the name of this script to us to show that you succeeded! This is optional.
    client.options['client_name'] = "asana_tasks_by_tag_id"

    lines = list()
    lines.append('${voffset 8}\\')
    # Iterate over the tags
    for tag_id in config.get('tag-ids'):
        tag = client.tags.get_tag(tag_id, opt_fields=['name'], opt_pretty=True)
        lines.extend(extract_tasks_from_tag(tag, client))

    # for debug
    # [print(line) for line in lines]

    line_string = ""
    for line in lines:
        line_string += line + "\n"

    # print_to_file(config.get('tagged_tasks')['output_path'], lines)
    replace_text_in_file(config.get('tagged_tasks')['output_path'], config.get('tagged_tasks')['start_tag'], config.get('tagged_tasks')['end_tag'], line_string)


if __name__ == '__main__':
    by_tag_label()
    # by_tag_id()
