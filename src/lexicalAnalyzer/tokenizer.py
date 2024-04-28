# Copyright (C), 2024-2025, bl33h 
# FileName: tokenizer.py
# Author: Sara Echeverria
# Version: I
# Creation: 29/03/2024
# Last modification: 06/04/2024

from directDfa.regexUtilities import getTransitionSymbols, getAcceptanceStates, getAcceptanceTokenStates
from lexicalAnalyzer.tokenUtilities import *
import pickle

class tokenizer():
    def __init__(self, nameFile, inputFile):
        self.name = nameFile
        
        with open(self.name, 'rb') as f:
            # load the dfa and the definitions from pickle
            self.unpYalexDirectDfa = pickle.load(f)
            self.yalexDirectDfa = pickle.load(f)
            self.yalDefs = pickle.load(f)
            
        f.close()

        # --- clean the definitions ---
        self.cleanDefinitions = [] 
        
        for definition in self.yalDefs:
            self.cleanDefinitions.append(definition.actualCleanDefinition())

        # --- get the acceptance states and the tokens ---
        self.acceptedStates = getAcceptanceStates(self.unpYalexDirectDfa.acceptedStates, self.unpYalexDirectDfa.explicitTransitions)
        self.dicTokens = getTransitionSymbols(self.yalexDirectDfa.acceptedStates, self.yalexDirectDfa.explicitTransitions)
        self.allTokens = getAcceptanceTokenStates(self.yalexDirectDfa.acceptedStates, self.yalexDirectDfa.explicitTransitions)
        
        # --- get the string to analyze ---
        with open(inputFile, encoding='utf-8') as f:
            self.text = f.readlines()
            
        # --- get the equal states ---
        self.equalStates = {}
        for unpKey, value in self.acceptedStates.items():
            for procKey, procValue in self.allTokens.items():
                
                if value == procValue:
                    self.equalStates[procKey] = [unpKey]
                    
                else:
                    currentTransitions = True

                    for val in procValue:
                        if val not in value: 
                            currentTransitions = False
                        
                    if currentTransitions:
                        self.equalStates[procKey] = [unpKey]
    
    # --- simulate the dfa ---
    def simulate(self):
        a = tokenUtilities(self.unpYalexDirectDfa)
        return a.tokenSimulation(self.text)
    
    # --- tokens ---
    # get the token
    def getTokens(self, symbol, state):
        for unpKey, value in self.equalStates.items():
            if state in value:
                for procKey,procValue in self.dicTokens.items():
                    if symbol == procValue:
                        return self.dicTokens[procKey]

                if symbol == self.dicTokens[unpKey]:
                    return self.dicTokens[unpKey]
                else:
                    return self.dicTokens[unpKey]
        
            else:
                for unpKey, value in self.allTokens.items():
                    if value == self.acceptedStates[state] or value in self.acceptedStates[state]:
                        return self.dicTokens[unpKey]
    
    # print the tokens
    def tokensList(self, listTokens):
        resultTokens = []
        for token in listTokens:
            if(token[1] == 'Error'):
                print(f"→ Lexeme: {token[0]} | !No token found")
            else:
                temp = ""
                if "\n" in token[0] or token[0] == " " or token[0] == "":
                    temp = repr(token[0])
                else:
                    temp = token[0]
                print(f"→ Lexeme: {temp} | >Token: {self.getTokens(temp, token[1][0])}")
                resultTokens.append((temp, self.getTokens(temp, token[1][0])))
        
        return resultTokens
    
    # place the tokens in a list
    def currentTokens(self, actualTokensList):
        self.newListTokens = []
        for token in actualTokensList:
            if(token[1] == 'Error'):
                self.newListTokens.append((token[0], "Error"))
            else:
                self.newListTokens.append((token[0], self.getTokens(token[0], token[1][0])))

        return self.newListTokens
    
    # place the brackets 
    def bracketsIdentifier(self, stringC):
        openingBracket = stringC.find("{")
        closingBracket = stringC.rfind("}")
        if openingBracket >= 0 and closingBracket >= 0:
            return stringC[openingBracket+1:closingBracket].strip()
        else:
            return None
    
    # make the tokenizerReader (the .py generated file)
    def tokenizerBuilder(self, name):
        self.tokenizerFile = f"src/yalexTokensIdentifier/{name}TokensDetector.py"
            
        with open(self.tokenizerFile, "w", encoding="utf-8") as f:
            
            # header
            f.write("# Copyright (C), 2024-2025, bl33h\n")
            f.write("# File: A tokenizer for the yaleX file\n")
            f.write("# Author: Sara Echeverria")
            f.write("\n")
            
            # imports
            f.write("\nimport pickle\n")
            
            # variables
            f.write("word = 'word'\n")
            f.write("WORD = 'WORD'\n")
            f.write("NUMBER = 7\n")
            f.write("WHITESPACE = ' '\n")
            f.write("PLUS = '+'\n")
            f.write("TIMES = '*'\n")
            f.write("DOT = '.'\n")
            f.write("MINUS = '-'\n")
            f.write("PERCENTAGE = '%'\n")
            f.write("CHARACTER = '_'\n")
            f.write("DOLLAR = '$'\n")
            f.write("DIVIDE = '/'\n")
            f.write("TOKEN = '%' + 'token'\n")
            f.write("TWOPOINTS = ':'\n")
            f.write("FINISHDECLARATION = ';'\n")
            f.write("LPAREN = '('\n")
            f.write("RPAREN = ')'\n")
            f.write("EQUALS = '='\n")
            f.write("AND = '&'\n")
            f.write("GREATERCHAR = '<'\n")
            f.write("tokens = []\n")
            
            # load the tokens
            f.write(f"\nwith open('{name}Tokens', 'rb') as f:\n")
            f.write("\ntokens = pickle.load(f)\n\n")
            f.write("def tokenReturns(symbol):\n")
            
            # returns the token
            for element in self.cleanDefinitions:
                if(element[2] != 'Without a function'):
                    func = self.bracketsIdentifier(element[2])
                    f.write(f"\tif symbol == '{element[0]}':\n\t\t{func}\n")
            
            # methods
            f.write("\n\treturn symbol\n")
            f.write("\nfor token in tokens:\n")
            f.write("\tif(token[1] == '!Error'):\n")
            f.write("\t\tprint(f'→ Lexeme: {token[0]} | !No token found')\n")
            f.write("\telse:\n")
            f.write("\t\ttemp = ''\n")
            f.write("\t\tif '\\n' in token[0] or token[0] == ' ' or token[0] == '':\n")
            f.write("\t\t\ttemp = repr(token[0])\n")
            f.write("\t\telse:\n")
            f.write("\t\t\ttemp = token[0]\n")
            f.write("\t\tprint(f'→ Lexeme: {temp} | >Token: {tokenReturns(token[1])}')")