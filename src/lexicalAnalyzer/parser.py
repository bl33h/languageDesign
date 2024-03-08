# Copyright (C), 2024-2025, bl33h 
# FileName: reader.py
# Author: Sara Echeverria
# Version: I
# Creation: 06/03/2024
# Last modification: 07/03/2024
# References
# [Rosetta Code. (2023). Compiler/lexical analyzer. https://rosettacode.org/wiki/Compiler/lexical_analyzer#Python]

from directDfa.regexUtilities import *  

class yalexParser():
    def __init__(self, file):
        self.file = file
        self.finalRegex = ""
        self.offDefinitions = []
        self.definitionsCleaner = []
        self.rules = []
        self.tempRegex = ""

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

        for pos, cleanLine in enumerate(emptyLines):
            split_line_temp = cleanLine.strip().split("=", 1)
            if len(split_line_temp) == 2:
                leftSide, rightSide = (el.strip() for el in split_line_temp)
                if(leftSide.strip().split(" ")[0].lower() == "let"):
                    self.offDefinitions.append(cleanLine)
                elif(leftSide.strip().split(" ")[0].lower() == "rule"):
                    for i in range(pos, len(emptyLines)):
                        self.rules.append(emptyLines[i].strip())                     
                    break
                else:
                    er = leftSide.strip().split(" ")[0]
                    errors.append((None, leftSide, f"{er} not defined !error"))
            else:
                errors.append((None, split_line_temp[0], "assignment !error"))
        
        print("\n=> definitions:")
        for i in self.offDefinitions:
            print("\t","-"*30)
            print("\t-> ", i)
            print("\t","-"*30)

        for defin in self.offDefinitions:
            name_desc = defin.split('=', 1)
            name = name_desc[0].split(' ')[1]
            desc = name_desc[1].strip()
            if(desc.startswith('[') and desc.endswith(']')):
                if(self.hasEscapeChars(desc)):
                    asciiCodes = self.specialCharsList(desc)
                    regexAscii = self.asciiConvertion(asciiCodes)
                    newDef = defs(name, regexAscii)
                    self.definitionsCleaner.append(newDef)
                else:
                    if('-' in desc): 
                        ranges = self.placeRegexRanges(desc)
                        regexRanges = self.regexRanges(ranges)
                        newDef = defs(name, regexRanges)
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
                desc = self.descriptionStructure(desc)
                newDef = defs(name, desc)
                self.definitionsCleaner.append(newDef)
                
        print()

        if(self.rules != []):
            self.rules.remove(self.rules[0])
            self.tempRegex, self.tempProcessedRegex = self.regexByRules(self.rules)
            
            print("=> processed tokens and definitions:")
            for definition in self.definitionsCleaner:
                print("-"*40)
                print(definition.tokensFeatures())
                print("-"*40)
                print()
                
            ls = [l.label for l in self.tempRegex]
            self.finalRegex = self.getFinalRegex(self.tempRegex)
            self.processedFinalRegex = self.getFinalRegex(self.tempProcessedRegex)
            ls = [l.label if not l.isSpecialChar else repr(l.label) for l in self.finalRegex]
            print("=> infix regex:\n", "".join(ls))

        return (self.finalRegex, self.processedFinalRegex, self.definitionsCleaner)

    def hasEscapeChars(self, line):
        escCharacters = ['\\','\n', '\r', '\t', '\b', '\f', '\v', '\a']
        for i in escCharacters:
            if i in line:
                return True
        return False

    def specialCharsList(self, line):
        listAscii = []
        i = 0
        while i < len(line):
            if line[i] in "[]'":
                i += 1
                continue
            elif line[i] == '\\':
                if i < len(line) - 1 and line[i+1] == 't':
                    listAscii.append(ord('\t'))
                    i += 2
                    continue
                elif i < len(line) - 1 and line[i+1] == 'n':
                    listAscii.append(ord('\n'))
                    i += 2
                    continue
                elif i < len(line) - 1 and line[i+1] == 's':
                    listAscii.append(ord(' '))
                    i += 2
                    continue
            elif line[i] in (' ', '\t', '\n'):
                if (line[i] == ' '):
                    listAscii.append(ord(' '))
                else:
                    listAscii.append(ord(line[i]))
                i += 1
                continue
            else:
                i += 1

        return listAscii
    
    def asciiConvertion(self, asciiCodes):
        regexAscii = []
        currentSymbol = explicitSymbols('|')
        currentSymbol.setType(True)
        
        for code in asciiCodes:
            if(type(code) == str):
                sym = explicitSymbols(code)
                sym.setSpecialType(True)
                regexAscii.append(sym)
                regexAscii.append(currentSymbol)
            else:
                sym = explicitSymbols(chr(code)) 
                sym.setSpecialType(True)
                regexAscii.append(sym)
                regexAscii.append(currentSymbol)
        
        regexAscii = regexAscii[:-1]
        openParenSym = explicitSymbols('(')
        openParenSym.setType(True)
        closedParenSym = explicitSymbols(')')
        closedParenSym.setType(True)
        regexAscii.insert(0, openParenSym)
        regexAscii.append(closedParenSym)
        return regexAscii

    def placeRegexRanges(self, line):
        ranges = []
        line = line.replace("'", '')
        
        for pos, charac in enumerate(line):
            if charac in "[]'":
                continue
            else:
                if charac == '-':
                    start = ord(line[pos-1])
                    end = ord(line[pos+1])
                    ranges.append([start, end])
        return ranges
    
    def regexRanges(self, ranges):
        regexRanges = []
        newRanges = []
        currentSymbol = explicitSymbols('|')
        currentSymbol.setType(True)
        
        for i in ranges:
            elementsRange = []
            for j in range(i[0], i[1]+1):
                sym = explicitSymbols(chr(j))
                elementsRange.append(sym)
            newRanges.append(elementsRange)
        
        for currentRange in newRanges:    
            for symbol in currentRange:
                regexRanges.append(symbol)
                regexRanges.append(currentSymbol)
        
        regexRanges = regexRanges[:-1]
        openParenSym = explicitSymbols('(')
        openParenSym.setType(True)
        closedParenSym = explicitSymbols(')')
        closedParenSym.setType(True)
        regexRanges.insert(0, openParenSym)
        regexRanges.append(closedParenSym)
        return regexRanges

    def descriptionStructure(self, desc):
        desc = desc.replace('"', '').replace("'", '').replace(" ", "")
        newDesc = []
        elemCor = ''
        elem = ''
        inCor = False
        
        currentSymbol = explicitSymbols('|')
        currentSymbol.setType(True)
        
        for char in desc:         
            if char.isalnum():
                elem += char
            else:
                if elem != '':
                    sym = explicitSymbols(elem)
                    newDesc.append(sym)
                    
                if elem == '_':
                    sym = explicitSymbols(elem)
                    newDesc.append(sym)
                    
                if elem == '→':
                    sym = explicitSymbols(ord(elem))
                    newDesc.append(sym)
        
                if char == '[':
                    inCor = True
                    newSim = explicitSymbols('(')
                    newSim.setType(True)
                    newDesc.append(newSim)

                elif char == ']':
                    inCor = False
                    for i in elemCor:
                        news = explicitSymbols(i)
                        newDesc.append(news)
                        newDesc.append(currentSymbol)
                    newDesc.pop()
                    newSim = explicitSymbols(')')
                    newSim.setType(True)
                    newDesc.append(newSim)
                    elemCor = ''
                elif inCor:
                    elemCor += char
        
                sym2 = explicitSymbols(char)
                if char == '.':
                    newDesc.append(sym2)
                if char != '.' and char != '[' and char != ']' and not inCor:
                    if(sym2.label == '_'):
                        sym2.setType(False)
                        newDesc.append(sym2)
                    else:
                        sym2.setType(True)
                        newDesc.append(sym2)
                elem = ''
                
        openParenSym = explicitSymbols('(')
        openParenSym.setType(True)
        closedParenSym = explicitSymbols(')')
        closedParenSym.setType(True)
        newDesc.insert(0, openParenSym)
        newDesc.append(closedParenSym)
        return newDesc
    
    def regexByRules(self, rules):
        regextL = []
        regexSymbols = []
        currentSymbol = explicitSymbols('|')
        currentSymbol.setType(True)
        tempRules = []

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
        for TokenDef in rulesList:
            if type(TokenDef) == explicitSymbols and TokenDef.label == '|' and TokenDef.isOperator:
                continue
            else:
                parts = TokenDef[0].strip().split(" ", 1)  
                if len(parts) == 1:
                    listTokensDef.append([parts[0].strip(), None])
                else:
                    if(parts[0].strip() == 'â†’'):
                        listTokensDef.append(['\u2192', parts[1].strip()])
                    else:
                        listTokensDef.append([parts[0].strip(), parts[1].strip()])

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
        
        for symbol in regextL:
            sym = explicitSymbols(symbol)
            regexSymbols.append(sym)
            regexSymbols.append(currentSymbol)
                        
        regexSymbols = regexSymbols[:-1]
        newRegexcurrentSymbol = []
        
        for i, elem in enumerate(regexSymbols):
            if (not elem.isOperator) or i == 0:
                newRegexcurrentSymbol.append(elem)
            else:
                prevSym = newRegexcurrentSymbol[i-1]
                newSim = explicitSymbols('#'+prevSym.label) 
                newRegexcurrentSymbol.append(newSim)

        if newRegexcurrentSymbol[-1].label != '|':
            prevSym = newRegexcurrentSymbol[-1]
            newSim = explicitSymbols('#'+prevSym.label) 
            newRegexcurrentSymbol.append(newSim)
        
        finalRegexSymbols = []  
        for i in range(len(newRegexcurrentSymbol)):
            finalRegexSymbols.append(newRegexcurrentSymbol[i])
            if (i+1) % 2 == 0 and i != len(newRegexcurrentSymbol)-1:
                finalRegexSymbols.append(currentSymbol)
                
        return (regexSymbols, finalRegexSymbols)

    def isTerminal(self, token):
        for defi in self.definitionsCleaner:
            if (defi.name == token.label):
                if(defi.desc != None):
                    return False
        return True

    def getDefinitions(self, token):
        for defi in self.definitionsCleaner:
            if (defi.name == token.label):
                if(defi.desc != None):
                    return defi.desc

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

    def getFinalRegex(self, finalRegex):
        finalRegex = finalRegex
        newRegex = []
        actualRegex = self.tokensReader(finalRegex, newRegex)
        return actualRegex