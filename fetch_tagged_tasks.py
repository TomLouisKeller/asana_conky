# Here we get all the tasks with tags
# Here is how we do it: https://asana.com/developers/api-reference/tasks#query
# GET    /tags/{tag_gid}/tasks
# Need to figure out the tag id first: GET    /tags
# GET    /tags

import asana

from asana_conky.helper import replace_text_in_file  # , print_to_file
from asana_conky.configuration import Configuration
from asana_conky.task import Task
from asana_conky.tag import Tag


def by_tag_id():
    config = Configuration()

    # Construct an Asana client
    client = asana.Client.access_token(config.get('personal_access_token'))

    # Set things up to send the name of this script to us to show that you succeeded! This is optional.
    client.options['client_name'] = "asana_tasks_by_tag_id"

    tagged_tasks = dict()
    # Iterate over the tags
    for tag_id in config.get('tag-ids'):
        tag = client.tags.get_tag(tag_id, opt_fields=['name'], opt_pretty=True)
        tag = Tag(tag['gid'], tag['name'])
        tagged_tasks[tag] = extract_tasks_from_tag(tag, client)

    output_string = tagged_tasks_to_string(tagged_tasks)

    replace_text_in_file(config.get('tagged_tasks')['output_path'], config.get('tagged_tasks')['start_tag'], config.get('tagged_tasks')['end_tag'], output_string)


def extract_tasks_from_tag(tag: Tag, client: asana.Client):
    api_tasks = client.tasks.get_tasks_for_tag(tag.id, completed_since='now', opt_fields=['name', 'due_on', 'due_at'], opt_pretty=True)

    # Extract Tasks from API
    tasks = []
    for task in api_tasks:
        tasks.append(Task(task['gid'], task['name'], task['due_on'], task['due_at']))

    # Sort tasks
    tasks = sorted(tasks)

    return tasks


def tagged_tasks_to_string(tagged_tasks: dict):
    output = ""

    for tag in tagged_tasks.keys():
        # Format
        output += '${voffset 8}\\\n'
        output += '${goto 40}${font Bitstream Vera Sans:size=11}${color3}' + tag.name + '$color$font${voffset 2}\n'
        for task in tagged_tasks[tag]:
            output += '${goto 50}' + task.name + '\n'

    return output


if __name__ == '__main__':
    by_tag_id()
