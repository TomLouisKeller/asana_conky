import os
import re
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


def replace_text(file_path, start_tag, end_tag, lines):

    if file_path is None or start_tag is None or end_tag is None:
        print("Will not replace anything since file_path, start_tag or end_tag have not been provided")
        return

    # Read in the file
    with open(file_path, 'r') as file:
        filedata = file.read()

    print(f"filedata {filedata}")

    pattern = start_tag + ".*" + end_tag
    print(f"Pattern {pattern}")
    # regex = re.compile(r"^.*interfaceOpDataFile.*$", flags=re.MULTILINE)
    regex = re.compile(pattern, flags=re.MULTILINE)
    # regex = pattern
    print(f"regex {regex}")

    replaced = re.sub(regex, lines, filedata)
    #replaced = re.sub(pattern, lines, filedata, flags=re.MULTILINE)

    print(f"replaced {replaced}")

    # Write the file out again
    with open(file_path, 'w') as file:
        file.write(replaced)

    assert filedata != replaced

    return None
