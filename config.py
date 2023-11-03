import argparse
import logging
import os

logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s]: %(message)s', datefmt='%m-%d-%Y %H:%M:%S')

parser = argparse.ArgumentParser()
parser.add_argument("-d", "--dir", help="Root directory")

ROOT_DIR = parser.dir