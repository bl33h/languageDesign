# Copyright (C), 2024-2025, bl33h 
# FileName: reader.py
# Author: Sara Echeverria
# Version: I
# Creation: 06/03/2024
# Last modification: 10/03/2024
# References
# [Rosetta Code. (2023). Compiler/lexical analyzer. https://rosettacode.org/wiki/Compiler/lexical_analyzer#Python]

from lexicalAnalyzer.parserUtilities import *

class yalexParser():
    def __init__(self, file):
        self.definitionsCleaner = []
        self.offDefinitions = []
        self.finalRegex = ""
        self.tempRegex = ""
        self.file = file
        self.rules = []
        
    
    # constructs the regex by the rules
    def regexByRules(self, rules):
            regextL = []
            regexSymbols = []
            currentSymbol = explicitSymbols('|')
            currentSymbol.setType(True)
            tempRules = []

            # rules lines identifier
            for line in rules:
                line = line.replace("'", '')
                line = line.replace('"', '')
                line = line.strip()
                
                if(line[0] == '|'):
                    tempRules.append(currentSymbol)
                    tempRules.append(line[1:])
                else:
                    tempRules.append(line)

            rulesList = []
            tempLi = []
            tempEl = ""
            
            # list of the rules by element
            for element in tempRules:
                if(element == tempRules[-1]):
                    rulesList.append([element.strip()])
                if type(element) == explicitSymbols and element.label == '|' and element.isOperator:
                    tempLi.append(tempEl)
                    rulesList.append(tempLi)
                    rulesList.append(element)
                    tempLi = []
                    tempEl = ""
                else:
                    tempEl += element.strip()+" "
                
            listTokensDef = []
            
            # list of the tokens and their definitions
            for tokenDef in rulesList:
                if type(tokenDef) == explicitSymbols and tokenDef.label == '|' and tokenDef.isOperator:
                    continue
                else:
                    parts = tokenDef[0].strip().split(" ", 1)  
                    if len(parts) == 1:
                        listTokensDef.append([parts[0].strip(), None])
                    else:
                        if(parts[0].strip() == 'â†’'):
                            listTokensDef.append(['\u2192', parts[1].strip()])
                        else:
                            listTokensDef.append([parts[0].strip(), parts[1].strip()])

            # list of the names of the tokens
            for el in listTokensDef:
                name, func = el
                regextL.append(name.strip())
                
                for defi in self.definitionsCleaner:
                    if defi.name == name:
                        defi.func = func
            
                names = [defin.name for defin in self.definitionsCleaner]
                if name not in names:
                    newDef = defs(name, None, func)
                    self.definitionsCleaner.append(newDef)
            
            # list where each element from regextL is followed by the current symbol
            for symbol in regextL:
                sym = explicitSymbols(symbol)
                regexSymbols.append(sym)
                regexSymbols.append(currentSymbol)
                            
            regexSymbols = regexSymbols[:-1]
            newRegexcurrentSymbol = []
            
            # checks if the first element is not an operator
            for i, elem in enumerate(regexSymbols):
                if (not elem.isOperator) or i == 0:
                    newRegexcurrentSymbol.append(elem)
                else:
                    prevSym = newRegexcurrentSymbol[i-1]
                    newSim = explicitSymbols('#'+prevSym.label) 
                    newRegexcurrentSymbol.append(newSim)

            # checks if the last element is not an operator
            if newRegexcurrentSymbol[-1].label != '|':
                prevSym = newRegexcurrentSymbol[-1]
                newSim = explicitSymbols('#'+prevSym.label) 
                newRegexcurrentSymbol.append(newSim)
            
            finalRegexSymbols = []
            
            # new list creation where all second elements are followed by the current symbol
            for i in range(len(newRegexcurrentSymbol)):
                finalRegexSymbols.append(newRegexcurrentSymbol[i])
                if (i+1) % 2 == 0 and i != len(newRegexcurrentSymbol)-1:
                    finalRegexSymbols.append(currentSymbol)
                    
            return (regexSymbols, finalRegexSymbols)
    
    # checks if the token is terminal
    def isTerminal(self, token):
        for defi in self.definitionsCleaner:
            if (defi.name == token.label):
                if(defi.desc != None):
                    return False
        return True
    
    # gets the definitions of the token
    def getDefinitions(self, token):
        for defi in self.definitionsCleaner:
            if (defi.name == token.label):
                if(defi.desc != None):
                    return defi.desc
    
    # reads the tokens        
    def tokensReader(self, actualT, newRegex):
        for tok in actualT:
            if(not self.isTerminal(tok)):
                newRegex = self.tokensReader(self.getDefinitions(tok), newRegex)
            else:
                newSym = explicitSymbols(tok.label)
                newSym.setToken(tok.token)
                
                if(tok.isSpecialChar):
                    newSym.setSpecialType(True)
                
                if(tok.isOperator):
                    newSym.setType(True)
  
                newRegex.append(newSym)
        return newRegex
    
    # gets the final regex
    def getFinalRegex(self, finalRegex):
        finalRegex = finalRegex
        newRegex = []
        actualRegex = self.tokensReader(finalRegex, newRegex)
        return actualRegex

    # reads the yalex file [main method]
    def read(self):
        with open(self.file, 'r') as file:
            lines = file.readlines()
            
        emptyLines = []
        comment = False
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            temp = ""
            for symbol in range(len(line)):
                if not comment:
                    if line[symbol] == '(':
                        if line[symbol+1] == '*':
                            comment = True
                            continue
                        else:
                            temp += line[symbol]
                    else:
                        temp += line[symbol]
                else:
                    if line[symbol] == '*':
                        if line[symbol+1] == ')':
                            continue
                    elif line[symbol] == ')':
                        if line[symbol-1] == '*':
                            comment = False
                            continue
                    
            
            newLine = temp.strip()
            if newLine:
                emptyLines.append(temp.strip())
                
        errors = []

        # checks if the brackets are balanced
        for pos, cleanLine in enumerate(emptyLines):
            temporarySplit = cleanLine.strip().split("=", 1)
            if len(temporarySplit) == 2:
                leftSide, _ = (el.strip() for el in temporarySplit)
                if(leftSide.strip().split(" ")[0].lower() == "let"):
                    errorOccurred, result = bracketBalanceCheck(cleanLine)
                    if errorOccurred:
                        print(result)
                        print(f"in line: {pos+1}")
                        print("------- !check your yalex file -------")
                        raise Exception("terminating the process, fix the issue and try again.")
                    else:
                        self.offDefinitions.append(cleanLine)
                elif(leftSide.strip().split(" ")[0].lower() == "rule"):
                    for i in range(pos, len(emptyLines)):
                        self.rules.append(emptyLines[i].strip())                     
                    break
                else:
                    er = leftSide.strip().split(" ")[0]
                    errors.append((None, leftSide, f"{er} not defined !error"))
            else:
                errors.append((None, temporarySplit[0], "assignment !error"))
        
        # shows the information
        print("\n=> definitions:")
        for i in self.offDefinitions:
            print("\t-> ", i)

        # element processing from the definitions and description conversion to regex
        for defin in self.offDefinitions:
            symDescription = defin.split('=', 1)
            name = symDescription[0].split(' ')[1]
            desc = symDescription[1].strip()
            if(desc.startswith('[') and desc.endswith(']')):
                if(hasEscapeChars(desc)):
                    asciiCodes = specialCharsList(desc)
                    regexAscii = asciiConvertion(asciiCodes)
                    newDef = defs(name, regexAscii)
                    self.definitionsCleaner.append(newDef)
                else:
                    if('-' in desc): 
                        ranges = placeRegexRanges(desc)
                        regexRangesP = regexRanges(ranges)
                        newDef = defs(name, regexRangesP)
                        self.definitionsCleaner.append(newDef)
                    else:
                        desc = desc.replace('[', '').replace(']', '').replace('"', '').replace("'", "")
                        newregex = []
                        for ch in desc:
                            sym = explicitSymbols(ch)
                            currentSymbol = explicitSymbols('|')
                            currentSymbol.setType(True)
                            newregex.append(sym)
                            newregex.append(currentSymbol)
                            
                        newregex = newregex[:-1]
                        openParenSym = explicitSymbols('(')
                        openParenSym.setType(True)
                        closedParenSym = explicitSymbols(')')
                        closedParenSym.setType(True)
                        newregex.insert(0, openParenSym)
                        newregex.append(closedParenSym)
                        newDef = defs(name, newregex)
                        self.definitionsCleaner.append(newDef)
                                    
            else:
                desc = descriptionStructure(desc)
                newDef = defs(name, desc)
                self.definitionsCleaner.append(newDef)
                
        print()

        # processed tokens and definitions
        if(self.rules != []):
            self.rules.remove(self.rules[0])
            self.tempRegex, self.tempProcessedRegex = self.regexByRules(self.rules)
            
            print("=> processed tokens and definitions:")
            for definition in self.definitionsCleaner:
                print("_"*70)
                print(definition.tokensFeatures())
                print("_"*70)
                print()
            
            # new labels list from each element
            ls = [l.label for l in self.tempRegex]
            self.finalRegex = self.getFinalRegex(self.tempRegex)
            self.processedFinalRegex = self.getFinalRegex(self.tempProcessedRegex)
            ls = [l.label if not l.isSpecialChar else repr(l.label) for l in self.finalRegex]
            print("=> infix regex:\n", "".join(ls))
            
            # concatenation checker
            pfnErrorChecker = "".join([l.label for l in self.processedFinalRegex])
            errorOccurred, result = errorManagement(pfnErrorChecker)
            if errorOccurred:
                print(result)
                print("------- !check your yalex file -------")
                raise Exception("terminating the process, fix the issue and try again.")
            else: 
                return (self.finalRegex, self.processedFinalRegex, self.definitionsCleaner)