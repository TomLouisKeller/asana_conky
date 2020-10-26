import requests
from logging import Logger


class DataFetcher:

    def __init__(self, personal_access_token, logger: Logger):
        self.headers = {'Authorization': 'Bearer {personal_access_token}'.format(personal_access_token=personal_access_token)}
        self.logger = logger

    # Get all tasks in the "My Tasks"-List
    def fetch_users_tasks(self, user_task_list_gid):
        url = "https://app.asana.com/api/1.0/user_task_lists/{user_task_list_gid}/tasks".format(user_task_list_gid=user_task_list_gid)
        params = {'completed_since': 'now'}
        response = requests.get(url, params=params, headers=self.headers)
        response_json = response.json()
        return response_json

    # Get a Task based on it's gid
    def fetch_task(self, gid):
        url = "https://app.asana.com/api/1.0/tasks/{gid}".format(gid=gid)
        response = requests.get(url, headers=self.headers)
        response_json = response.json()
        return response_json
