# Command
# python3 [this script file name] [repo path]

"""
Expected output
- JSON File
- Content
{
    "c": [
        "./path/to/file.c",
    ],
    "cpp": [
        "./path/to/file.cpp",
    ],"
}
"""

import json
import os
import sys
from multiprocessing import Pool

import include # header file

# this file will be created
FILES_JSON='files.json'

# input in temrinal:
# python allFileMakefile.py repo
# argv[0] == allFileMakefile.py
# argv[1] == repo
dir_path = sys.argv[1]

def get_file_extension(file_path):
    """
    get file extension
    eg: version.txt
    result: txt
    """
    _, file_extension = os.path.splitext(file_path)
    file_extension = strip_element(file_extension, 1)
    return str(file_extension)

def strip_element(string, index):
    """
    To strip element from string.
    First element starts from 1
    """
    new_string = string[index:]
    return new_string



def get_file_name(file_path):
    """
    get file name, including file extension
    eg: full path = /data/a/b/c.txt
    result: c.txt
    """
    dir_path, file_name = os.path.split(file_path)
    return str(file_name)


def open_files_in_dir(dir_path, data):
    """
    to open all files in given directory
    a directory may consists of sub dir
    in that case, need to recursively call the function again
    if is a file, open it
    This function use `yield` method, something related to `function generator` try google it
    """
    for file_name in os.listdir(dir_path):
        print('Writting ' + file_name)
        file_path = os.path.join(dir_path, file_name)

        # if is dir, recursively call the function again to open it
        if os.path.isdir(file_path):
            # `yield from` is only supported on python 3.3 above
            # so, run command `python3 [python file]`
            yield from open_files_in_dir(file_path, data)
        else:
            # dont want store file name only, some file name duplicates, store full path instead
            # file_name = get_file_name(file_path)
            file_extension = get_file_extension(file_name)
            yield file_path, file_extension



def main():
    include.create_file(FILES_JSON)
    data = dict()
    for file_name, file_extension in open_files_in_dir(dir_path, data):
        data = include.update_dictionary(file_extension, file_name, data)
    include.write_json(data, FILES_JSON)

# with Pool() as pool:
#     pool,map(main(), range(10)

main()