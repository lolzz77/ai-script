# Command
# python3 [this script file name]

"""
Expected output
- JSON File
- Content
{
    "dir": null,
    "char": null,
    "proc": null,
}
"""

import json
import re
import os
import sys
from multiprocessing import Pool

import include # header file

# this is existing JSON file
C_FUNCTIONS_JSON='cFunctions.json'
# this is newly created by this script
ACRONYM_JSON='acronym.json'


def main():
    # get data
    with open(C_FUNCTIONS_JSON, 'r') as f:
        data = json.load(f)

    # create file
    include.create_file(ACRONYM_JSON) 

    # get all values, from all keys
    values = []
    for key in data.keys():
        values.extend(data[key])

    # start splitting string
    results = []
    for value in values:
        results.extend(include.spiltString(value))

    # remove duplicates
    list_to_set = set(results)
    results = list(list_to_set)

    # update dictionary
    data_acronym = {}
    for result in results:
        # the value of the dictionary will be in list
        data_acronym = include.update_dictionary(result, [None], data_acronym)

    # write to file
    include.write_json(data_acronym, ACRONYM_JSON)

main()