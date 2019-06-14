import os
from time import gmtime, strftime

def get_current_location():
    return os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

def get_absolute_path(filename: str):
    return os.path.join(get_current_location(), filename)

def get_logger():
    from datetime import datetime
    import logging
    import sys

    logging_path = "tmp/{now}.log".format(now=str(datetime.now()))
    level = logging.DEBUG
    format = '%(asctime)s - %(lineno)d - %(message)s'

    format = logging.Formatter(format)

    logger = logging.RootLogger(level)

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(format)
    console_handler.setLevel(level)
    logger.addHandler(console_handler)

    #file_handler = logging.FileHandler(logging_path)
    #file_handler.setFormatter(format)
    #file_handler.setLevel(level)
    #logger.addHandler(file_handler)

    return logger

# Return today's date
def get_date_today():
    return strftime("%Y-%m-%d", gmtime())

def print_to_file(output_file_path, content: list):
    file = open(output_file_path,"w") 
    for line in content:
        file.write(line + "\n")
    file.close() 