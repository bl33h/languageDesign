# Copyright (C), 2024-2025, bl33h 
# FileName: parserUtilities.py
# Author: Sara Echeverria
# Version: I
# Creation: 08/03/2024
# Last modification: 08/03/2024
# References
# [Rosetta Code. (2023). Compiler/lexical analyzer. https://rosettacode.org/wiki/Compiler/lexical_analyzer#Python]

from directDfa.regexUtilities import *  

# check if the line has escape characters
def hasEscapeChars(line):
        escCharacters = ['\\','\n', '\r', '\t', '\b', '\f', '\v', '\a']
        
        for i in escCharacters:
            if i in line:
                return True
        return False

# special characters list
def specialCharsList(line):
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

# ascii convertion
def asciiConvertion(asciiCodes):
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

# place the regex ranges [1.]
def placeRegexRanges(line):
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

# place the regex ranges [2.]
def regexRanges(ranges):
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

# place the description structure
def descriptionStructure(desc):
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

# rules bracket balance check
def bracketBalanceCheck(line):
        openBrackets = 0
        for char in line:
            if char == '[':
                openBrackets += 1
            elif char == ']':
                openBrackets -= 1
                if openBrackets < 0: 
                    return (True, "error: unmatched closing bracket.")
        
        if openBrackets > 0:
            return (True, "error: unmatched opening bracket.")
        
        return (False, "")