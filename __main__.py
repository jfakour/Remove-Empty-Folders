import os
import logging 
import argparse
from pathlib import Path

def sizelimit_type(i):
    i = int(i)
    if i < 0:
        raise argparse.ArgumentTypeError("Minimum size limit is 0")
    return i

logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s]: %(message)s', datefmt='%m-%d-%Y %H:%M:%S')

parser = argparse.ArgumentParser()
parser.add_argument("-d", "--dir", help="Root directory", default="")
parser.add_argument("-hl", "--headless", help="Including this argument sets HEADLESS_MODE: True", action='store_true')
parser.add_argument("-s", "--sizelimit", type=sizelimit_type, help="Include all folders <= sizelimit (bytes)", default=0)
args = parser.parse_args()

HEADLESS_MODE = args.headless
SIZE_LIMIT = args.sizelimit
logging.info(f"This application will recursively search a root directory and remove folders smaller than {SIZE_LIMIT} bytes.")
IGNORE_DICT = {}

def find_empty_folders(path: str, size_limit: int):
    result = {}
    for root, folders, files in os.walk(path, topdown=False):
        for f in folders:
            f_path = os.path.join(root, f)
            if f_path not in IGNORE_DICT:
                f_size = get_size(f_path)
                if not os.listdir(f_path) or f_size <= size_limit:
                    result[f_path] = f_size

    return result

def get_size(path: str):
    result = 0
    for root, folders, files in os.walk(path, topdown=False):
        for f in files:
            f_path = os.path.join(root, f)
            if not os.path.islink(f_path):
                result += os.path.getsize(f_path)
    return result


def get_root_dir_from(path: str):
    result = path
    while not os.path.exists(result):
        result = input(f"'{result}' does not exist. Enter a new path: ")
        result = result.replace("'", "")
        result = result.replace('"', "")
    return result

def remove_dirs_from(dir_list: list):
    for d in dir_list:
        for f in os.listdir(d):
            remove_single_item(f)
        remove_single_item(d)

def remove_single_item(file_or_dir: str):
    if (remove_single_item in IGNORE_DICT):
        logging.info(f"IGNORED '{file_or_dir}'")
    try:
        if os.path.isfile(file_or_dir):
            os.remove(file_or_dir)
            t = 'File'
        else:
            os.rmdir(file_or_dir)
            t = 'Folder'
        logging.info(f"{t} '{file_or_dir}' removed")
    except PermissionError as pe:
        IGNORE_DICT[file_or_dir] = "Permissions Error"
        logging.warning(f"Permissions Error: {file_or_dir} added to Ignore List")

def print_list(d: dict):
    keys = d.keys()
    for i in keys:
        logging.info(f"* '{i}' {d[i]} bytes")

def removal_prompt():
    if HEADLESS_MODE:
        return True
    selection = input('Enter [Y]es to remove the directories above > ')
    selection = selection.upper()
    return selection == 'Y' or selection == 'YES'


if __name__ == "__main__":
    ROOT_DIR = get_root_dir_from(args.dir)
    HEADLESS_MODE = False if ROOT_DIR != args.dir else HEADLESS_MODE
    HL_Str = "ON" if HEADLESS_MODE else "OFF"
    logging.warning(f"HEADLESS MODE: {HL_Str}")
    e_dir_dict = find_empty_folders(ROOT_DIR, SIZE_LIMIT)

    while (len(e_dir_dict) > 0):
        logging.info("******************************************************") 
        logging.info("* The following Files/Folders will be ignored:        ")   
        print_list(IGNORE_DICT)
        logging.info("* ----------------------------------------------------") 

        logging.info("******************************************************") 
        logging.info("* The following directories are marked for removal: ")   
        print_list(e_dir_dict)
        logging.info("* ----------------------------------------------------")  
        if not removal_prompt():
            break
        remove_dirs_from(e_dir_dict)
        e_dir_dict = find_empty_folders(ROOT_DIR, SIZE_LIMIT)

    logging.info("Exiting Application.")


