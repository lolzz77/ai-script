# Command
# python3 [this script file name]

"""
Expected output
- this is my acronym json
{
    "passwd" : ["password"]
}

This new JSON will be created
{
    "path/to/c/file": 
    [
        {
            "functionName" : "get_passwd",
            "acronymTags" : ["get", "passwod"]
        },
        {
            "functionName" : "save_passwd",
            "acronymTags" : ["save", "passwod"]
        }
    ],
    "path/to/c/file": 
    [
        {
            "functionName" : "get_passwd",
            "acronymTags" : ["get", "passwod"]
        },
        {
            "functionName" : "save_passwd",
            "acronymTags" : ["save", "passwod"]
        }
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
ACRONYM_JSON='acronym.json'
C_FUNCTIONS_JSON='cFunctions.json'
# this is new JSON file that will be created
C_FUNCTION_TAGS_JSON='cFunctionTags.json'


def main():
    include.create_file(C_FUNCTION_TAGS_JSON)

    data_write = {}

    inner_data_write = {
        "functionName" : "",
        "acronymTags" : []
    }

    with open(C_FUNCTIONS_JSON, 'r') as f:
        c_function_data = json.load(f)

    with open(ACRONYM_JSON, 'r') as f:
        acronym_data = json.load(f)

    for key in c_function_data.keys():
        the_path = key
        the_list = c_function_data[key]
        data_write[the_path] = None
        for i, function_name in enumerate(the_list):
            inner_data_write = {
                "functionName" : "",
                "acronymTags" : []
            }
            if data_write[the_path] is None:
                data_write[the_path] = [inner_data_write]
            else:
                data_write[the_path].append(inner_data_write)
            data_write[the_path][i]['functionName'] = function_name
            split_list = include.spilt_string(function_name)
            for word in split_list:
                if word in acronym_data.keys():
                    data_write[the_path][i]['acronymTags'].extend(acronym_data[word])

    include.write_json(data_write, C_FUNCTION_TAGS_JSON)

main()