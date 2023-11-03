import os
import logging 
import argparse
from pathlib import Path

logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s]: %(message)s', datefmt='%m-%d-%Y %H:%M:%S')

parser = argparse.ArgumentParser()
parser.add_argument("-d", "--dir", help="Root directory", default="")
parser.add_argument("-hl", "--headless", help="Headless Mode: True", action='store_true')
args = parser.parse_args()

HEADLESS_MODE = args.headless
logging.info("This application will recursively search a root directory and remove empty folders.")

def find_empty_folders(path: str):
    result = []
    for root, folders, files in os.walk(path, topdown=False):
        for f in folders:
            f_path = os.path.join(root, f)
            if not os.listdir(f_path):
                result.append(f_path)
    return result

def get_root_dir_from(path: str):
    result = path
    while not os.path.exists(result):
        result = input(f"'{result}' does not exist. Enter a new path: ")
        result = result.replace("'", "")
        result = result.replace('"', "")
    return result

def remove_dirs_from(dir_list: list, print= True):
    for d in dir_list:
        os.rmdir(d)
        if print:
            logging.info(f"'{d}' removed.")

def print_list(l: list):
    for i in l:
        logging.info(f"* '{i}'")

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
    e_dir_list = find_empty_folders(ROOT_DIR)

    while (len(e_dir_list) > 0):
        logging.info("******************************************************") 
        logging.info("* The following directories are marked for removal: ")   
        print_list(e_dir_list)
        logging.info("* ----------------------------------------------------")  
        if not removal_prompt():
            break
        remove_dirs_from(e_dir_list)
        e_dir_list = find_empty_folders(ROOT_DIR)

    logging.info("Exiting Application.")


