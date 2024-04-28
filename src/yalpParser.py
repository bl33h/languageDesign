# Copyright (C), 2024-2025, bl33h 
# FileName: yalpParser.py
# Author: Sara Echeverria
# Version: I
# Creation: 27/04/2024
# Last modification: 28/04/2024

# import sys
# sys.path.append('C:\\Users\\sarap\\OneDrive\\Escritorio\\languageDesign\\src')

from directDfa.directDfaBuilder import displayLR0
from directDfa.regexUtilities import *
import pickle

class yalpParser():
    def __init__(self, file, tokensYal, numberFile):
        self.file = file
        self.tokensYalp = []
        self.grammar = []
        self.grammarSymbols = []
        self.productions = []
        self.finalLines = []
        self.numberFile = numberFile
        self.checkProductions = {}
    
        with open(tokensYal, 'rb') as f:
            pickle.load(f)
            pickle.load(f)
            self.tokensY = pickle.load(f)