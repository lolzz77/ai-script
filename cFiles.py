# Command
# python3 [file name] [json file that has list of all files according to their file extension] [file extension]

import json
import os
import sys
import re

import include # header file

from multiprocessing import Pool

FILES_JSON='cFiles2.json'

# input in temrinal:
# python allFileMakefile.py repo
# argv[0] == allFileMakefile.py
# argv[1] == repo
json_file_path = sys.argv[1]
file_extension = sys.argv[2]

# data = include.parse_json(json_file_path)
# files_path = data[str(file_extension)]
# for file_path in files_path:
#     with open(file_path, 'r') as f:
#          for line in f:
#             tokens = line.strip().split()
#             print(tokens)

# this regex will match '//' and '/**/', multi-line supported
comment_regex = r'\/\/.*|\/\*[\s\S]*?\*\/'
# extract function name
# eg: static int main(int x) & int main(int x)
# result: 'main'
function_name_regex = r'\b(\w+)\s*\('

data = include.parse_json(json_file_path)
files_path = data[str(file_extension)]

data_dict = dict()

include.create_file(FILES_JSON)

for file_path in files_path:
    with open(file_path, 'r') as f:
        data = ''
        try:
            data = f.read()
        except UnicodeDecodeError as e:
            print('Skipping ' + file_path)
            write_buffer = include.update_dictionary('skip', file_path, data_dict)
        # detect and store all comments, in a list
        # it will store like this
        # ['//comment', '/* multi line comment * * end*/']
        # for multi-line comment, it will store all lines into one element
        comments = re.findall(comment_regex, data)
        # remove comment, replacing them with ''
        for comment in comments:
            data = data.replace(comment, '')
        # transform data read into each individual line in list
        # eg: "hello, hi
        #      there"
        # result: ['hello, hi', 'there']
        lines = data.splitlines()
        print('Writting ' + file_path)
        for line in lines:
            # if match ANY one of regex in include.POSIX_regex_match
            # and do not match ANY and NOT ONE (means all) regex in include.POSIX_regex_skip
            if any(re.search(regex, line) for regex in include.POSIX_regex_match) and all(not re.search(regex, line) for regex in include.POSIX_regex_skip):
                function_name_group = re.search(function_name_regex, line)
                if function_name_group:
                    # function_name_group will print rubbish
                    # .group(1) will print the result found
                    function_name = function_name_group.group(1)
                    write_buffer = include.update_dictionary(file_path, function_name, data_dict)

include.write_json(write_buffer, FILES_JSON)

                