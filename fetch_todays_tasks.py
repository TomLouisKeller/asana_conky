## Get all tasks that are due today or prior to today
# Unfortunately the asana api doesn't let us query
# by due date or at least by assignee_status = inbox
# so we have to get all the tasks in the "My Tasks"
# list and then fetch one after another to get the due date
# and sort out the one's that have a due date prior to, 
# and including today
from helper import print_to_file, get_logger
from configuration import Configuration
from asana_service import AsanaService
from data_fetcher import DataFetcher

# Get configuration
config = Configuration()
personal_access_token = config.get('personal_access_token')
user_task_list_gid = config.get('user_task_list_gid')
output_file_path = config.get('output_file_path')

logger = get_logger()

# Here the magic happens
def main():
    data_fetcher = DataFetcher(personal_access_token)
    asana_service = AsanaService(data_fetcher)

    # Fetch all tasks from the "My Tasks" list
    tasks = data_fetcher.fetch_users_tasks(user_task_list_gid)
    tasks = tasks['data']

    # Remove all tasks that aren't due today or prior to that
    tasks = asana_service.filter_due_tasks(tasks)

    # Create labels(simple text strings) from tasks
    logger.debug("Due today tasks:")
    task_labels = asana_service.extract_task_labels(tasks)

    # Sort tasks by due date
    task_labels = asana_service.sort_task_labels(task_labels)

    # Print labels to file
    print_to_file(output_file_path, task_labels)

    logger.debug('Done')

main()