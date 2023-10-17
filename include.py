import re
import json
import nltk
nltk.download('words')
from nltk.corpus import words

COLORS = {
    'reset'         : '\x1b[0m',
    'underline'     : '\x1b[4m',
    'reverse'       : '\x1b[7m',
    'red'           : '\x1b[31m',
    'green'         : '\x1b[32m',
    'yellow'        : '\x1b[33m',
    'blue'          : '\x1b[34m',
    'magenta'       : '\x1b[35m',
    'cyan'          : '\x1b[36m',
    'white'         : '\x1b[37m',
    'grey'          : '\x1b[90m',
    'lightred'      : '\x1b[1;31m',
    'lightgreen'    : '\x1b[1;32m',
    'lightyellow'   : '\x1b[1;33m',
    'lightblue'     : '\x1b[1;34m',
    'lightmagenta'  : '\x1b[1;35m',
    'lightcyan'     : '\x1b[1;36m',
}

POSIX_regex_skip = [
    # If matches these, skip
    #0
    "^[ ]*inline",
    #1
    "^[ ]*[#][ ]*define",
    #2
    "^[ ]*[#][ ]*if[ ]+[(]*defined",
    #3
    "^[ ]*[#][ ]*if[(]*defined",
    #4
    "^[ ]*[#][ ]*ifndef",
    #5
    "^[ ]*if[ ]*\\(",
    #6
    "^[ ]*else[ ]*\\{",
    #7
    "^[ ]*else if[ ]*\\(",
    #8
    "^[ ]*switch[ ]*\\(",
    #9
    "^[ ]*case[ ]*[^:]+[ ]*:",
    #10
    "^[ ]*return[ ]*[^;]+[ ]*[;?,&&|]",
    #11
    "^[ ]*typedef[ ]*",
    #12
    "^[ ]*union[ ]*",
    #13
    "^[ ]*for[ ]*\\(",
    #14
    "^[ ]*do[ {]*", 
    #15
    "^[ ]*while[ ]*\\(",
    #16
    "^[ (]*[a-zA-Z0-9()_*]+[)]*[ ][a-zA-Z0-9_*]+[ ]*::[ ]*operator", 
    #17
    "^[a-zA-Z0-9_*]+::[~a-zA-Z0-9_*]+[ (]+",
    #18
    "^[ ]*[a-zA-Z0-9()_*]+[ ]+[a-zA-Z0-9()_*]+[[]*[0-9]+[]]*[ ]*=[ ]*[{ ]*[^}]*[}]",
]
POSIX_regex_match = [
    # If matches these, write 
    # for constructor & destructor, they dont have function return type
    # so basically they are already filtered out
    #0
    "^[ (]*[a-zA-Z0-9_*]+[)]*[ ]+[a-zA-Z0-9_*]+[ ]*[(][^{)]*[)][ ]*", # void test()
    #1
    "^[ (]*[a-zA-Z0-9_*]+[)]*[ ]+[a-zA-Z0-9_*]+[ ]+[a-zA-Z0-9_*]+[ ]*[(][^{)]*[)][ ]*", # void __static test()
    #2
    "^[ (]*[a-zA-Z0-9_*]+[)]*[ ]+[a-zA-Z0-9_*]+[ ]+[a-zA-Z0-9_*]+[ ]+[a-zA-Z0-9_*]+[ ]*[(][^{)]*[)][ ]*", # static/extern int FAST_FUNC test()
    #3
    "^[ (]*[a-zA-Z0-9_*]+[)]*[ ]+[a-zA-Z0-9_*]+[ ]*[::][ ]*[a-zA-Z0-9_*]+[ ]*[(][^{)]*[)][ ]*", # void class::func()
]

FILE_EXTENSION_MAKEFILE = '*.mk'

FILE_EXTENSION = [
    ".c",
    ".cpp"
]

GIT_IGNORE_CMD = 'git check-ignore -v'

# Compile a list of regex
regex_list_skip = [
    re.compile(POSIX_regex_skip[0]),
    re.compile(POSIX_regex_skip[1]),
    re.compile(POSIX_regex_skip[2]),
    re.compile(POSIX_regex_skip[3]),
    re.compile(POSIX_regex_skip[4]),
    re.compile(POSIX_regex_skip[5]),
    re.compile(POSIX_regex_skip[6]),
    re.compile(POSIX_regex_skip[7]),
    re.compile(POSIX_regex_skip[8]),
    re.compile(POSIX_regex_skip[9]),
    re.compile(POSIX_regex_skip[10]),
    re.compile(POSIX_regex_skip[11]),
    re.compile(POSIX_regex_skip[12]),
    re.compile(POSIX_regex_skip[13]),
    re.compile(POSIX_regex_skip[14]),
    re.compile(POSIX_regex_skip[15]),
    re.compile(POSIX_regex_skip[16]),
    re.compile(POSIX_regex_skip[17]),
    re.compile(POSIX_regex_skip[18]),
]
regex_list_match = [
    re.compile(POSIX_regex_match[0]),
    re.compile(POSIX_regex_match[1]),
    re.compile(POSIX_regex_match[2]),
    re.compile(POSIX_regex_match[3])
]

def parse_json(file_path):
    """
    prase jason data
    resulting data returned is a dictionary type
    """
    with open(file_path, 'r') as f:
        data = json.load(f)
    return data


def write_json(data, file_path):
    with open(file_path, 'w') as f:
        json.dump(data, f)

def update_dictionary(key, value, data):
    """
    update the dictionary
    dictionary use this format { 'key' : 'value' }
    If key exists, it will append to value, will not overwrite the value

    data: this param is essential. This is the dictionary data return by this function
    You can pass in empty 'data', then this dictionary will write data into it
    """
    if key == '':
        key = 'unknown'

    if key not in data:
        data[key] = value
    else:
        # check if the value is list or not
        # Because dictionary is key : Value
        # the value is not a list
        # you gotta convert it to list
        if not isinstance(data.setdefault(key, []), list):
            data[key] = [data[key]]
        data[key].append(value)

    return data


def create_file(file_path):
    """
    always create a file, if file exists, erase and create
    """

    open(file_path, 'w').close()

    # this coding checks if exists
    # if not os.path.exists(file_path):
    #     open(file_path, 'w').close()
    #     return True
    # return False

def detect_case(string):
    """
    To detect what string (eg: camel, pascal, snake, kebab)
    But i found out, this probably not a good approach
    Especially for mixed case (eg: camel + snake)
    """
    isCamel = False
    isSnake = False
    isKebab = False
    isPascal = False
    matched = 0
    result = ''

    if snakeCaseRegex.search(string):
        isSnake = True
    if kebabCaseRegex.search(string):
        isKebab = True
    if camalCaseRegex.search(string):
        isCamel = True
    if pascalCaseRegex.search(string):
        isPascal = True

    if isCamel:
        matched+=1
        result = 'camel'
    if isSnake:
        matched+=1
        result = 'snake'
    if isKebab:
        matched+=1
        result = 'kebab'
    if isPascal:
        matched+=1
        result = 'pascal'
    
    if matched>1:
        return 'mixed'
    elif matched==0:
        return 'unknown'
    else:
        return result

def spilt_string(string):
    """
    To split a string (camel, pascal, snake, kebab) altogether
    """
    listOfWords = []
    result = []

    if '_' in string:
        listOfWords.extend(string.split('_'))
    if '-' in string:
        listOfWords.extend(string.split('-'))
    if any(c.isdigit() for c in string): # If contain digits
        listOfWords.extend(re.split(r'(\d+)', string))

    if listOfWords == []:
        listOfWords.append(string)

    for words in listOfWords:
        # fail, `MSG` will split `m,s,g`
        # splitted_words = re.findall(r'[a-z]+|[A-Z][a-z]*', words)
        # fail, `MSGTo` will split `MSGT, o`
        # splitted_words = re.findall(r'[A-Z]?[a-z]+|[A-Z]+', words)
        splitted_words = re.findall(r'[A-Z]?[a-z]+|[A-Z]+(?=[A-Z][a-z]|$)', words)
        if splitted_words:
            result.extend(splitted_words)
        else:
            result.append(words)
    # fail, this will lower `MSG`
    # i dont wan it to lower if the whole string is uppercase
    # `Hello` -> lower
    # `HELLO` dont lower
    # lowerCased = [s.lower() for s in result]
    lowerCased = [s.lower() if any(c.islower() for c in s) else s for s in result]
    return lowerCased

def is_english_word(word):
    """
    return: True / False
    eg: "eur" - False
    "your" - True
    """
    return word in words.words()