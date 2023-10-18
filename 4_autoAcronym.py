# Command
# python3 [this script file name]
# this file will auto insert acronym that has 'None' value
# Will insert according to python NLTK dictionary
# the rest unknown words, will leave it 'None'

# Note: this scipt might take some time

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
    "dir": null,
    "char": null,
    "proc": proc,
}

"""

import json
import re
import os
import sys
from multiprocessing import Pool
import nltk
nltk.download('words')
from nltk.corpus import words

import include # header file

# this is existing JSON file
ACRONYM_JSON='acronym.json'
MY_ACRONYM_JSON='my-acronym.json'

def is_english_word(word):
    return word in words.words()

def main():
    with open(ACRONYM_JSON, 'r') as f:
        acronym_data = json.load(f)

    with open(MY_ACRONYM_JSON, 'r') as f:
        my_acronym_data = json.load(f)

    values = []
    for key in acronym_data.keys():
        if acronym_data[key][0] is None:
            if include.is_english_word(key):
                acronym_data[key][0] = key
            for my_acronym_key in my_acronym_data.keys():
                if key == my_acronym_key:
                    acronym_data[key] = my_acronym_data[key]
    
    include.write_json(acronym_data, ACRONYM_JSON)

main()