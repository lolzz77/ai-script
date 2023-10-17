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

to be updated into

{
    "dir": directory,
    "char": character,
    "proc": proc,
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

def check():
    """
    to check how many acronyms are answered and how many are not
    results:
    Total: 54233
    Is none: 0
    Is not none: 54233
    """


def main():
    # get data
    with open(ACRONYM_JSON, 'r') as f:
        data = json.load(f)

    values = []
    total = 0
    is_none = 0
    is_not_none = 0
    for key in data.keys():
        total += 1
        if len(data[key]) == 1 and data[key][0] is None:
            print(key)
            is_none += 1
        else:
            is_not_none += 1
    
    print('Total: '+str(total))
    print('Is none: '+str(is_none))
    print('Is not none: '+str(is_not_none))
    
main()