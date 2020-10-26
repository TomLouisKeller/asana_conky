import os
from time import gmtime, strftime


def get_current_location():
    return os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))


def get_absolute_path(filename: str):
    if filename.startswith('/'):
        # print("root -> ", filename)
        return filename
    elif filename.startswith('~/'):
        # print("home -> ", filename)
        return filename
    elif filename.startswith('../'):
        # print("../ -> ", filename)
        return os.path.join(get_current_location(), filename)
    else:
        # print("relative ->  ", filename)
        return os.path.join(get_current_location(), "../", filename)


# Return today's date
def get_date_today():
    return strftime("%Y-%m-%d", gmtime())


def print_to_file(output_file_path, content: list):
    file = open(output_file_path, "w")
    for line in content:
        file.write(line + "\n")
    file.close() 
