from __future__ import unicode_literals, print_function, division
from io import open
import glob
import os
import unicodedata
import string

filepath = "./data/identifiers/"

class fileToArray:
    def __init__(self, filepath ):
        self.filepath = filepath
        self.n_categories = 0
        # Build the category_lines dictionary, a list of names per language
        self.category_lines = {}
        self.all_categories= []
        self.defineAttr()

    def findFiles(self, path): return glob.glob(path)

    # Turn a Unicode string to plain ASCII, thanks to https://stackoverflow.com/a/518232/2809427
    def unicodeToAscii(self, s):
        all_letters = string.ascii_letters + " .,;'"
        n_letters = len(all_letters)
        return ''.join(
            c for c in unicodedata.normalize('NFD', s)
            if unicodedata.category(c) != 'Mn'
            and c in all_letters
        )

    # Read a file and split into lines
    def readLines(self, filename):
        lines = open(filename, encoding='utf-8').read().strip().split('\n')
        return [self.unicodeToAscii(line) for line in lines]

    def defineAttr(self):
        for filename in self.findFiles(self.filepath + '*.txt'):
            category = os.path.splitext(os.path.basename(filename))[0]
            self.all_categories.append(category)
            lines = self.readLines(filename)
            self.category_lines[category] = lines

        self.n_categories = len(self.all_categories)
    

test= fileToArray(filepath)
print(test.all_categories)
