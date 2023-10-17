# pip install nltk

import re
import nltk
nltk.download('words')
from nltk.corpus import words

camalCaseRegex = re.compile(r'^[a-z]+[^_-]+') # camalCase
pascalCaseRegex = re.compile(r'^[A-Z]+[^_-]+') # PascalCase
snakeCaseRegex = re.compile(r'.*_.*') # snake_case
kebabCaseRegex = re.compile(r'.*-.*') # Kebab-Case

import unittest
from collections import Counter
import include



class TestSplitString(unittest.TestCase):
    # def test_detect_case(self):
    #     test_cases = [
    #         ['thisIsCamelCase',                      'camel'],
    #         ['this_is_snake_case',                   'snake'],
    #         ['this-is-kebab-case',                   'kebab'],
    #         ['ThisIsPascalCase',                     'pascal'],
    #         ['this_isMixtureOfSnakeAndCamelCase',    'mixed'],
    #     ]

    #     for i, test_case in enumerate(test_cases):
    #         # doing this way, it will output which test case failed
    #         # 1st index is 0
    #         with self.subTest(i=i):
    #             self.assertEqual(detect_case(test_case[0]), test_case[1])

    def test_split_string(self):
        test_cases = [
            # If is acronym, return UPPERCASE
            # If is capitalized letter, return all in lowercase
            ['thisIsCamelCase',                    ['this', 'is', 'camel', 'case']],
            ['thisiscancer',                       ['thisiscancer']],
            ['this_is_snake_case',                 ['this', 'is', 'snake', 'case']],
            ['this-is-kebab-case',                 ['this', 'is', 'kebab', 'case']],
            ['ThisIsPascalCase',                   ['this', 'is', 'pascal', 'case']],
            ['this_isMixtureOfSnakeAndCamelCase',  ['this', 'is', 'mixture', 'of', 'snake', 'and', 'camel', 'case']],
            ['MSG',                                ['MSG']],
            ['sendMSG_toReceiver',                 ['send', 'MSG', 'to', 'receiver']],
            ['SendMSGToReceiver',                  ['send', 'MSG', 'to', 'receiver']],
            ['cancerstringbutthen_got_this_betterAndAlsoTGIFYahoo', ['cancerstringbutthen', 'got', 'this', 'better', 'and', 'also','TGIF', 'yahoo']],
            ['hi', ['hi']],
            ['add', ['add']],
            ['a', ['a']],
            ['HAHA_lolAreYouOK', ['HAHA', 'lol', 'are', 'you', 'OK']],
            ['XIntX', ['X', 'int', 'X']],
            ['XCharX', ['X', 'char', 'X']],
            # logically, this is how it will be splitted
            # unless your dictionary detects that `Xint` is not a word
            # and finds that, `int` is a word, and thus separate them into `X, int`
            # I shall see how should I fix this
            ['Xint', ['xint']],
            ['XintX', ['xint', 'X']],
            ['A2A', ['A', '2']], # duplicates will be removed
            ['pause2continue', ['pause', '2', 'continue']],
            ['A_B_', ['A', 'B']],
            ['_A_B', ['A', 'B']],
            ['_A_B_', ['A', 'B']],
            ['A_B-C', ['A', 'B', 'C']],
            ['A_123', ['A', '123']],
            ['A_B_123', ['A', 'B', '123']],
            ['_A_B_123_', ['A', 'B', '123']],
            ['-A_B_123-', ['A', 'B', '123']],
            ['-A_B-123_', ['A', 'B', '123']],
            ['--A_B--123__', ['A', 'B', '123']],
        ]

        for i, test_case in enumerate(test_cases):
            # doing this way, it will output which test case failed
            # 1st index is 0

            with self.subTest(i=i):
                self.assertEqual(Counter(include.spilt_string(test_case[0])), Counter(test_case[1]))

class TestIsEnglishWord(unittest.TestCase):
    def test_is_english_word(self):
        test_cases = [
            ['your', True],
            ['Your', False],
            ['ur', True],
            ['eur', False],
        ]

        # # to print all words
        # print(words.words())

        # # to print words that start with certain character
        # ur_words = [word for word in words.words() if word.startswith('eur')]
        # print(ur_words)

        for i, test_case in enumerate(test_cases):
            test = test_case[0]
            result = test_case[1]
            with self.subTest(i=i):
                self.assertEqual(include.is_english_word(test), result)

if __name__ == '__main__':
    unittest.main()
