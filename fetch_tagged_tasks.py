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
                lines.append('${voffset 8}\\')
            lines.extend(extract_tasks_from_tag(tags[config_tag_name], client))

    [print(line) for line in lines]

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

    is_first = True
    lines = list()
    for tag_id in config.get('tag-ids'):
        tag = client.tags.get_tag(tag_id, opt_fields=['name'], opt_pretty=True)

        if is_first:
            is_first = False
        else:
            lines.append('${voffset 8}\\')

        lines.extend(extract_tasks_from_tag(tag, client))

    # [print(line) for line in lines]

    line_string = ""
    for line in lines:
        line_string += line + "\n"

    # print_to_file(config.get('tagged_tasks')['output_path'], lines)
    replace_text_in_file(config.get('tagged_tasks')['output_path'], config.get('tagged_tasks')['start_tag'], config.get('tagged_tasks')['end_tag'], line_string)


if __name__ == '__main__':
    # by_tag_label()
    by_tag_id()
