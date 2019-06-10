import requests
import json
from configuration import Configuration

# Get configuration
config = Configuration()
personal_access_token = config.get('personal_access_token')
user_task_list_gid = config.get('user_task_list_gid')

url = "https://app.asana.com/api/1.0/user_task_lists/{user_task_list_gid}/tasks".format(user_task_list_gid=user_task_list_gid)

params = {'completed_since': 'now', 'assignee_status': 'inbox'}
headers = {'Authorization': 'Bearer {personal_access_token}'.format(personal_access_token=personal_access_token)}

response = requests.get(url, params=params, headers=headers)
response_json = response.json()
result = json.dumps(response_json, sort_keys=False, indent=2)
print(result)