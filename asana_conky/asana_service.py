
import asana

from .configuration import Configuration
from .task import Task
from .tag import Tag


def get_tasks_for_tag(tag: Tag, client: asana.Client):
    api_tasks = client.tasks.get_tasks_for_tag(tag.id, completed_since='now', opt_fields=['name', 'due_on', 'due_at'])

    # Extract Tasks from API
    tasks = []
    for task in api_tasks:
        tasks.append(Task(task['gid'], task['name'], task['due_on'], task['due_at']))

    # Sort tasks
    tasks = sorted(tasks)

    return tasks


def tagged_tasks_to_string(tagged_tasks: dict, config: Configuration):
    output = ""
    for tag in tagged_tasks.keys():
        output += tag_to_string(tag, config)
        for task in tagged_tasks[tag]:
            output += replace_task_in_string(config.get('tagged_tasks')['task_format'], task, config)
    return output


def tag_to_string(tag: Tag, config: Configuration):
    return config.get('tagged_tasks')['tag_format'] \
                 .replace('{tag_id}', tag.id) \
                 .replace('{tag_name}', tag.name)


def replace_task_in_string(source_string: str, task: Task, config: Configuration):
    return source_string.replace('{task_id}', task.id) \
                        .replace('{task_name}', task.name) \
                        .replace('{task_due_date}', task.due_date.strftime(config.get('date_format')) if task.due_date else "") \
                        .replace('{task_due_time}', task.due_time.strftime(config.get('time_format')) if task.due_time else "")
