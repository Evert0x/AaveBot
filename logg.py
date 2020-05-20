import logging
import os

formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s')

def get(file, name):
    handler = logging.FileHandler(file)
    handler.setLevel(logging.INFO)
    handler.setFormatter(formatter)

    log = logging.getLogger(name)
    log.setLevel(logging.INFO)
    log.addHandler(handler)

    return log


# Log
ERROR = get(os.path.join("log", "error.log"), "ERROR")