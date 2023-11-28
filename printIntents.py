# command
"""
1. prett yprint json content
- can add `| less` after the command
python3 [this script file name] [json file]

2. Search some keyword in JSON
- [search] - the keyword for this operation
- [layer] - json file has many layers, which layer you want to print
- [item] - either `key` or `value`
- [search string] - the keyword you want to search
python3 [this script file name] [json file] search [layer] [item] [search string]

3. 
python3 [this script file name] [json file] one [layer(json file has many layers, which layer you want to print)] [item(dictionary, key or value)]

4. search function backronyms
- [backronym] - the keyword for this operation
- [search string] - the backronym keyword you want to search
python3 [this script file name] [json file] backronym [search string]
"""

import sys
import argparse
import json
import include # header file

# # with this, you can pass in argument like this
# # python3 printIntents.py --layer 2 --item 1
# # if you didnt pass anything, it will be None
# parser = argparse.ArgumentParser()
# parser.add_argument('--layer', type=int, help='the layer to print')
# parser.add_argument('--item', type=int, help='the layer to print')
# args = parser.parse_args()

# if args.layer is None:
#     print('No layer specified')
# else:
#     print(args.layer)

operation_pretty_print = False
operatoin_search = False
operatoin_one_item = False
operatoin_one_layer = False
json_file_path = None
layer = None
item = None
key = None
search_str = None

# input in temrinal:
# python allFileMakefile.py repo
# argv[0] == allFileMakefile.py
# argv[1] == repo
json_file_path = sys.argv[1]
if len(sys.argv) == 2:
    operation_pretty_print=True
if len(sys.argv) >= 3:
    if sys.argv[2] == 'search':
        operatoin_search=True
        layer = int(sys.argv[3])
        item = str(sys.argv[4])
        search_str = str(sys.argv[5])
    elif sys.argv[2] == 'one':
        operatoin_one_item=True
        layer = int(sys.argv[3])
        key = str(sys.argv[4])
    elif sys.argv[2] == 'print':
        operatoin_one_layer=True
        layer = int(sys.argv[3])
    elif sys.argv[2] == 'backronym':
        operatoin_backronym=True
        search_str = str(sys.argv[3])


def print_json_by_layers(data, layer = 1, item = 'key'):
    """
    To print json data layer by layer

    param:
    data    - this is parsed json data, it will be in dictionary format
    layer   - 1 = 1st layer = 1,3,8
    item    - key or value. Json is like dictionary, { key : value }
            - 1: key, 2: value

    Imagine this is json data
    data = {
        "1": "a",
        "3": "b",
        "8": {
            "12": "c",
            "25": "d"
        }
    }
    Depending on passed in parameter
    layer - 1; item - key
    output: 1, 3, 8
    layer - 1; item - value
    output: a, b, {'25': 'd', '12': 'c'}
    layer - 2; item - key
    output: 12, 25
    layer - 2; item - value
    output: c, d

    If the inner is list, it is supported as well
    data = {
        "1": "a",
        "3": "b",
        "8": [
            '12',
            '25'
        ]
    }
    """

    if layer == 1:
        for key, value in data.items():
            # Print either key or value, depending on the passed in parameter
            print(key if item == 'key' else value)
    else:
        for key, value in data.items():
            # Check if the value is dictionary or not
            # If yes, then recursively call the function again
            if isinstance(value, dict):
                print_json_by_layers(value, layer - 1, item)
            # if is a list, just call a for loop to print
            # a list will not be having 'inner layer'
            if isinstance(value, list):
                for v in value:
                    print(v)

def get_last_element(data):
    """
    path = a/b/c/d.txt
    this functio will return 'd.txt
    """
    
    # split = data.split('/')[-1]
    # last_element = split[-1]
    # return last_element

    return data.split('/')[-1]

def operation_pretty_print_json(data):
    """
    print json data in pretty format
    indent = 4 means 4 indentation
    """
    pretty_json = json.dumps(data, indent=4)
    print(pretty_json)

def search_json(data, layer, item, search_str):
    """
    """
    if layer == 1:
        for key, value in data.items():
            if search_str in (key if item == 'key' else value):
                print(key if item == 'key' else value)
    else:
        for key, value in data.items():
            # Check if the value is dictionary or not
            # If yes, then recursively call the function again
            if isinstance(value, dict):
                print_json_by_layers(value, layer - 1, item)
            # if is a list, just call a for loop to print
            # a list will not be having 'inner layer'
            if isinstance(value, list):
                for v in value:
                    print(v)

def print_json_one_item(data, key):
    if layer == 1:
        pretty_json = json.dumps(data[key], indent=4)
        print(pretty_json)
    else:
        for key, value in data.items():
            print_json_one_item(value, layer - 1, key)

def print_json_layer(data, layer):
    if layer == 1:
        for key, value in data.items():
            print(key)
    else:
        for key, value in data.items():
            print_json_layer(value, layer - 1)

def print_backronym(data, search_str):
    """
    intended for json file that has the following format:
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

    print result:
    file path: path/to/file
    function name: functionName
    """
    for key, value in data.items():
        file_path_printed = False
        if value is None:
            continue
        for v in value:
            if v["acronymTags"] is None:
                continue
            if search_str in v["acronymTags"]:
                if not file_path_printed:
                    file_path_printed = True
                    print()
                    print(include.COLORS['yellow'] + "File Path : " + key + include.COLORS['reset'])
                print(v["functionName"])

    
data = include.parse_json(json_file_path)

if operation_pretty_print:
    operation_pretty_print_json(data)
    sys.exit()

if operatoin_search:
    search_json(data, layer, item, search_str)
    sys.exit()

if operatoin_one_item:
    print_json_one_item(data, key)
    sys.exit()

if operatoin_one_layer:
    print_json_layer(data, layer)
    sys.exit()

if operatoin_backronym:
    print_backronym(data, search_str)
    sys.exit()

# for value in data[str(item)]:
#     print(get_last_element(value))
# print(data[str(item)])
# print_json_by_layers(data , layer, item)


