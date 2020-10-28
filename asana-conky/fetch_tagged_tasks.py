# Here we get all the tasks with tags
# Here is how we do it: https://asana.com/developers/api-reference/tasks#query
# GET    /tags/{tag_gid}/tasks
# Need to figure out the tag id first: GET    /tags
# GET    /tags

import asana
# from datetime import datetime
from helper import print_to_file
from configuration import Configuration


def extract_tasks_from_tag(tag, client):
    # tasks = client.tasks.get_tasks_for_tag(config.get('user_task_list_gid'), completed_since='now', opt_fields=opt_fields, opt_pretty=True)
    opt_fields = ['name', 'due_on', 'due_at']
    tasks = client.tasks.get_tasks_for_tag(tag['gid'], completed_since='now', opt_fields=opt_fields, opt_pretty=True)

    # # Sort tasks by due date
    # req_tasks = sorted(req_tasks, key=lambda task: task['due_at'] if task['due_at'] else task['due_on'])

    # Format
    lines = list()
    lines.append("# {}".format(tag['name']))
    for task in tasks:
        # due_on = ""
        # if config.get('show_time') is False:
        #     due_on = datetime.fromisoformat(dt['due_on']).strftime("%d.%m")
        # elif dt['due_at'] is None:  # maybe we have to remove the '        ' if there no items do have due_at
        #     due_on = datetime.fromisoformat(dt['due_on']).strftime("%d.%m") + '        '
        # else:
        #     due_on = datetime.fromisoformat(dt['due_at'][:-1]).strftime("%d.%m %H:%M")

        # TODO: show due_on and/or due_at if available
        lines.append(task['name'])
    return lines


# TODO: In order to respect the order of the tags-names in the config, we have to first fetch all and then iterate over the config-tag-names-list
def by_tag_label():
    config = Configuration()

    # Construct an Asana client
    client = asana.Client.access_token(config.get('personal_access_token'))

    # Set things up to send the name of this script to us to show that you succeeded! This is optional.
    client.options['client_name'] = "asana_tasks_by_tag_name"

    tags = client.tags.get_tags({'workspace': config.get('workspace_gid')}, opt_fields=['name'], opt_pretty=True)

    lines = list()
    is_first = True
    for tag in tags:
        if tag['name'] in config.get('tag-names'):
            if is_first:
                is_first = False
            else:
                lines.append("")
            lines.extend(extract_tasks_from_tag(tag, client))

    # [print(line) for line in lines]

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


by_tag_id()
