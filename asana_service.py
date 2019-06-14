import requests
from data_fetcher import DataFetcher
from helper import get_date_today, get_logger

class AsanaService:

    def __init__(self, data_fetcher: DataFetcher):
        self.logger = get_logger()
        self.data_fetcher = data_fetcher

    def fetch_parent_task_label(self, parent):
        if parent is not None and 'gid' in parent and 'name' in parent:
            self.logger.debug("Parent gid: {} name: {}".format(parent['gid'], parent['name']))

            parent = self.data_fetcher.fetch_task(parent['gid'])['data']
            parents_name_string = self.fetch_parent_task_label(parent['parent'])

            if parents_name_string is not "":
                parents_name_string += " - > "

            parents_name_string += parent['name']

            return parents_name_string
        else:
            return ""

    # To test fetch_parent_task_label
    # logger.debug(fetch_parent_task_label(dict({'gid':'1125180580548326', 'name':'Conky'})))

    # Remove all tasks that aren't due today or prior to that
    def filter_due_tasks(self, tasks):
        today = get_date_today()
        due_tasks = list()
        for task in tasks:
            self.logger.debug("FromAllTasks: {} - {}".format(task['gid'], task['name']))
            due_on = self.extract_due_on(task['gid'])
            if due_on is not None and due_on <= today:
                due_tasks.append(task)
        return due_tasks

    # Get the due-on parameter of a task
    def extract_due_on(self, gid):
        data = self.data_fetcher.fetch_task(gid)
        return data['data']['due_on']

    def extract_task_labels(self, tasks):
        task_labels = list()
        for task in tasks:
            self.logger.debug(task['name'])
            task_labels.append(self.extract_task_label(task['gid']))
        return task_labels

    # Create label from task
    # Format: #date# - #parent_name# -> #name#
    def extract_task_label(self, gid):
        task = self.data_fetcher.fetch_task(gid)['data']
        
        task_label = task['due_on'] + " -> "

        # Recursively get the names of all parent tasks
        self.logger.debug('Get parent of task: {}'.format(task['name']))

        parents_name_string = self.fetch_parent_task_label(task['parent'])
        if parents_name_string is not "":
                parents_name_string += " - > "

        task_label += parents_name_string
        
        task_label += task['name']

        self.logger.debug("DueToday: {} - {}".format(task['gid'], task['name']))
        self.logger.debug(self.data_fetcher.fetch_task(task['gid']))

        return task_label

    # Sort the tasks in the list by due_date
    def sort_task_labels(self, tasks):
        tasks.sort()
        return tasks
