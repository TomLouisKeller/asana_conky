# Here we get all the tasks with tags
# Here is how we do it: https://asana.com/developers/api-reference/tasks#query
# GET    /tags/{tag_gid}/tasks
# Need to figure out the tag id first: GET    /tags
# GET    /tags

import asana

from asana_conky.helper import replace_text_in_file
from asana_conky.asana_service import get_tasks_for_tag, tagged_tasks_to_string, replace_task_in_string, tag_to_string
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
        tag = client.tags.get_tag(tag_id, opt_fields=['name'])
        tag = Tag(tag['gid'], tag['name'])
        tagged_tasks[tag] = get_tasks_for_tag(tag, client)

    output_string = tagged_tasks_to_string(tagged_tasks, config)

    replace_text_in_file(config.get('tagged_tasks')['output_path'], config.get('tagged_tasks')['start_tag'], config.get('tagged_tasks')['end_tag'], output_string)


if __name__ == '__main__':
    by_tag_id()
