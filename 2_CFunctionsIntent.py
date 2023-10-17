# Command
# python3 [this script file name] [langauge]
# Note: If it takes 8 hours to complete, something wrong with your code
# I found that `matches_function` list is not freed. Thus, the list getting larger n larger
# Then only it dump into JSON file

"""
Expected output
- JSON File
- Content
{
    "path/to/c/file": [
        "main",
        "getDir",
        "getChar",
    ]
}
"""

import json
import re
import os
import sys
from multiprocessing import Pool

import include # header file

# this is existing JSON file
FILES_JSON='files.json'
# this is newly created by this script
C_FUNCTIONS_JSON='cFunctions.json'

pattern = r'\b([a-zA-Z_][a-zA-Z0-9_]*)\s*\([^)]*\)\s*\{'
symbolic_words = ['\\t', '\\r', '\\n']
not_a_function = ['if', 'for', 'while', 'switch', 'else', 'else if']

# def main():
#     with open(FILES_JSON, 'r') as f:
#         data = json.load(f)

#     c_files_path = data.get('c')
#     lines = []
#     for c_file_path in c_files_path:
#         with open(c_file_path, 'rb') as f:
#             for line in f:
#                 try:
#                     lines.append(line.decode('utf-8'))
#                 except UnicodeDecodeError:
#                     pass
#             for line in lines:
#                 try:
#                     # print(line.encode('utf-8'))
#                     print(line.encode('ascii', errors='ignore'))
#                 except UnicodeDecodeError:
#                     pass


def main():
    with open(FILES_JSON, 'r') as f:
        data = json.load(f)

    include.create_file(C_FUNCTIONS_JSON) 

    # get the 'key' of the JSON file
    c_files_path = data.get('c')

    data_c_function_name = {}
    function_matches = []
    i = 0
    for c_file_path in c_files_path:
        print('Reading: ' + c_file_path)
        # read in binary mode
        with open(c_file_path, 'rb') as f:
            # convert binary to string
            binary_string = str(f.read())
            # remove all the \t, \r, \n
            for symbols in symbolic_words:
                # replace it to whitespace, else, it will stick 2 words tgt
                binary_string = binary_string.replace(symbols, ' ')
            # find the function name
            matches = re.findall(pattern, binary_string)
            # remove not a function matches
            for match in matches:
                if match not in not_a_function:
                    function_matches.append(match)
            # remove duplicates
            list_to_set = set(function_matches)
            function_matches = list(list_to_set)
            # print(function_matches)
            # update the dictionary
            data_c_function_name = include.update_dictionary(c_file_path, function_matches, data_c_function_name)
            # write to JSON
            # have to reset this, else, in loop, this list will just grow bigger n bigger, containing past items
            # might as well at the same time reset all
            function_matches = []
            list_to_set = None
            binary_string = None
            matches = None

    include.write_json(data_c_function_name, C_FUNCTIONS_JSON)

main()