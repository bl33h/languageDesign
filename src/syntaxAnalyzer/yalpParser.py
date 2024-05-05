# Copyright (C), 2024-2025, bl33h 
# name: yalpParser.py
# Author: Sara Echeverria
# Version: I
# Creation: 27/04/2024
# Last modification: 28/04/2024

from directDfa.directDfaBuilder import displayLR0, displayLR0Diagram
from directDfa.regexUtilities import *
import pickle

class yalpParser():
    def __init__(self, file, tokensYal, name):
        self.checkProductions = {}
        self.yalpFileTokens = []
        self.grammarSymbols = []
        self.productions = []
        self.finalLines = []
        self.grammar = []
        self.name = name
        self.file = file
        
        # load tokens from the pickle file
        with open(tokensYal, 'rb') as f:
            pickle.load(f)
            pickle.load(f)
            self.tokensY = pickle.load(f)
    
    # ------------------- reading function -------------------
    def read(self):
        with open(self.file, 'r', encoding="utf-8") as file:
            lines = file.readlines()
            
        comment = False
        
        for line in lines:
            line = line.strip()
            
            if not line:
                continue
                        
            temp = ""
            
            # comment verification
            for symbol in range(len(line)):
                if not comment:
                    if line[symbol] == '/':
                        if line[symbol+1] == '*':
                            comment = True
                            continue
                        else:
                            temp += line[symbol]
                    else:
                        temp += line[symbol]
                else:
                    if line[symbol] == '*':
                        if line[symbol+1] == '/':
                            continue
                    elif line[symbol] == '/':
                        if line[symbol-1] == '*':
                            comment = False
                            continue
            
            # grammar verification            
            if '->' in line or '→' in line:
                if ('->' in line):
                    line = line.replace('->', '→')
                    
                beginning = line.find("/*") + 2
                ending = line.rfind("*/")
                subchain = line[beginning:ending].strip()
                self.grammar.append(subchain) 
                    
            newLine = temp.strip()
            if newLine:
                self.finalLines.append(temp.strip())  
        
        # tokens verification        
        tokensYa = []
        self.tokenBrackets = {}
        for i in self.tokensY:
            a = i.actualCleanDefinition()
            
            if a[2] != 'Without a function':
                bracketsVal = self.yalexTokensIdentifier(self.bracketsInformation(a[2]))
                tokensYa.append(bracketsVal)
                if (a[0] not in self.tokenBrackets):
                    self.tokenBrackets[bracketsVal] = a[0]
            else:
                self.tokenBrackets[a[0]] = None

        # productions verification
        productionLines = self.tokens(tokensYa)
        production = []
        
        for line in productionLines:
            if (len(line) == 1 and line[0] == ';') and line.endswith(";"):
                self.productions.append(" ".join(production))
                production = []
            else:  
                production.append(line)
            
        print("------ Grammar ------") 
        for i in self.grammar:
            print(i)
               
        print("\n------ Yalp Tokens ------")
        for i in self.yalpFileTokens:
            print(i)
            
        print("\n------ Productions ------")
        newProductions = []
        for i in self.productions: 
            temp = i.split(" ")
            newP = []
            for t in temp:
                if t.isupper():
                    newP.append(t)
                    continue
                else:
                    newP.append(t)
            i = " ".join(newP)
            newProductions.append(i)
            print(i)
        
        # productions elements
        self.productions = newProductions
        newProductions = []
        for production in self.productions:
            tempLine = production.split(" ")
            tempNewProduction = []
            for elem in tempLine:
                if elem == tempLine[0]:
                    tempNewProduction.append(elem+" →")
                else:
                    tempNewProduction.append(elem)
            newProductions.append(" ".join(tempNewProduction))

        dotItem = itemsInTheProductions('°')
        self.finalProductions = []
        dotItem.setFinal(True)
        self.terminals = []
        
        # elements in the productions
        for element in newProductions:
            arrow = "→"
            if ("->" in element):
                arrow = "->"
            elif ("→" in element):
                arrow = "→"
                
            sides = element.split(arrow)
            sides = [elem.strip() for elem in sides]
            rightList = []

            for prod in [x.strip() for x in sides[1].split("|")]:
                productionsList = []
                
                for elem in prod.split(" "):
                    if(elem.isupper()):
                        newItem = itemsInTheProductions(elem, self.tokenBrackets[elem])
                        newItem.setType(True)
                        productionsList.append(newItem)
                        self.terminals.append(elem)
                    else:
                        if elem in [x.lower() for x in self.tokensVeri]:
                            newItem = itemsInTheProductions(elem.upper(), self.tokenBrackets[elem.upper()])
                            newItem.setType(True)
                            productionsList.append(newItem)
                            self.terminals.append(elem.upper())
                        else:
                            newItem = itemsInTheProductions(elem, elem[0].upper())
                            newItem.setType(False)
                            productionsList.append(newItem)

                rightList.append(productionsList)
               
            for rightS in rightList: 
                newT = itemsInTheProductions(sides[0].strip().replace(":",""), sides[0].strip()[0].upper())
                newT.setType(False)
                self.finalProductions.append(actualProductions(newT, rightS))
                
        self.temporaryProductions = self.finalProductions

        self.initialSymbols = self.finalProductions[0].ls
        increased = self.finalProductions[0].ls
        newItemB = itemsInTheProductions(f"{increased}'")
        newIncreasedP = actualProductions(newItemB, [dotItem, increased])
        self.increasedEl = increased
        self.increasedElB = newItemB
        self.finalProductions.insert(0, newIncreasedP)        
        
        print("\n------ Final productions ------")
        for x in self.finalProductions:
            print(x)
        print()
                     
        self.newFinalStates(newIncreasedP)
        
        print()
    
    # ------------------- grammar symbols function -------------------
    def getGrammarSymbols(self):
        self.grammarSymbol = set()
        
        for i in self.finalProductions:
            for j in i.rs:
                if j.dot:
                    continue
                else:
                    self.grammarSymbol.add(j.label)
            self.grammarSymbol.add(i.ls.label)
                
        self.grammarSymbols = sorted(list(self.grammarSymbol))
    
    # ------------------- closure function -------------------            
    def closure(self, productions):
        dotItem = itemsInTheProductions('°')
        dotItem.setFinal(True)
        finalSet = productions
        for prod in finalSet:
            for i in range(len(prod.rs)):
                if(prod.rs[i].dot):
                    if(i+1 < len(prod.rs)):
                        if(not prod.rs[i+1].terminal):
                            for produ in self.finalProductions:
                                if produ.ls.label == prod.rs[i+1].label:
                                    if(not any([v.dot for v in produ.rs])):
                                        produ.rs.insert(0, dotItem)
                                    if produ not in finalSet:
                                        finalSet.append(produ)
        
        return finalSet
    
    # ------------------- go to function -------------------
    def goTo(self, items, symbol):
        newState = []
        for prod in items:
            for i in range(len(prod.rs)):
                if(prod.rs[i].dot):
                    if(i+1 < len(prod.rs)):
                        comp = [k for k, v in self.tokenBrackets.items() if v == symbol]
                        if(prod.rs[i+1].label == symbol or prod.rs[i+1].label == (comp[0] if len(comp)>0 else None)):
                            productionsIndex = prod.rs.index([x for x in prod.rs if x.dot][0])
                            if productionsIndex < len(prod.rs):
                                newPrRS = prod.rs.copy()
                                temp = prod.rs[productionsIndex+1]
                                newPrRS[productionsIndex+1] = prod.rs[productionsIndex]
                                newPrRS[productionsIndex] = temp
                                newProd = actualProductions(prod.ls, newPrRS)
                                newState.append(newProd)

        return self.closure(newState)
    
    # ------------------- first function -------------------
    def first(self, symbol):
        productionsChecker = [symbol]
        stack = [symbol]
        firstSet = []
        
        # if the symbol is a terminal, return the symbol
        if symbol in self.terminals:
            return stack
        else:
            while stack:
                check = stack.pop(0)
                for prod in self.finalProductions:
                    if prod.ls.label == check:
                        if prod.rs[0].label in self.terminals:
                            firstSet.append(prod.rs[0].label)
                        else:
                            if prod.rs[0].label not in stack and prod.rs[0].label not in productionsChecker:
                                stack.append(prod.rs[0].label)
                                productionsChecker.append(prod.rs[0].label)
        
        return firstSet
        
    # ------------------- following function -------------------       
    def following(self, symbol):
        followingSet = []
        
        if(symbol == self.initialSymbols.label):
            followingSet.append('$')
        
        for prod in self.finalProductions:
            for i in range(len(prod.rs)):
                if(symbol == prod.rs[i].label):
                    if(prod.rs[i].label == prod.rs[-1].label):
                        fol = self.following(prod.ls.label)
                        for el in fol:
                            if el not in followingSet:
                                followingSet.append(el)
                    if ((i+1) < len(prod.rs)):
                        firs = self.first(prod.rs[i+1].label)
                        for el in firs:
                            if el not in followingSet:
                                followingSet.append(el)

        return followingSet
    
   # ------------------- new final states function -------------------
    def newFinalStates(self, increased):
        self.getGrammarSymbols()
        statesNumber = 0
        finalStates = {}
        C = self.closure([increased])
        finalStates[f"I{statesNumber}"] = C
        transitions = []
        items = [C]
        
        # items
        for group in items:
            for symbol in self.grammarSymbols:
                result = self.goTo(group, symbol)
                
                if result != []:
                    if result not in finalStates.values():
                        items.append(result)
                        statesNumber += 1
                        finalStates[f"I{statesNumber}"] = result
                        
                        for k, v in finalStates.items():
                            if v == group:
                                transitions.append(explicitTransitions(k, symbol, f"I{statesNumber}"))
                    else:
                        for k, v in finalStates.items():
                            if v == group:
                                for k2, v2 in finalStates.items():
                                    if v2 == result:
                                        transitions.append(explicitTransitions(k, symbol, k2))
        
        # states & features
        lr0Descriptions = {}
        
        for k, v in finalStates.items():
            itemsDescription = [str(el) for el in v if el is not None]
            if itemsDescription:
                lr0Descriptions[k] = "\n".join(itemsDescription)
        
        finState = None
        inState = None
        
        print("\n------------------------ LR0 diagram ------------------------")
                    
        for k,v in finalStates.items():
            print(k, len(v))
            for el in v:
                if el.ls.label == self.increasedElB.label:
                    for i in range(len(el.rs)):
                        if el.rs[i].label == self.increasedEl.label and el.rs[i-1].dot:
                            finState = k
                            break
                    for i in range(len(el.rs)):
                        if(i+1 < len(el.rs)):
                            if el.rs[i].dot and el.rs[i+1].label == self.increasedEl.label:
                                inState = k
                                break
                print(el)
                print("_"*50)
            print("\n")
    
        lr0 = automatonInfo(inState, [finState], len(finalStates.keys()), transitions, list(finalStates.keys()))
        displayLR0(lr0, f"LR0{self.name}")
        displayLR0Diagram(lr0, f"LR0{self.name}Diagram", lr0Descriptions)

    # ------------------- brackets information function -------------------
    def bracketsInformation(self, text):
        openingBracket = text.find("{")
        closingBracket = text.rfind("}")
        if openingBracket >= 0 and closingBracket >= 0:
            return text[openingBracket+1:closingBracket].strip()
        else:
            return None
    
    # ------------------- get the yalex file tokens function -------------------
    def yalexTokensIdentifier(self, text):
        if text is not None:
            return text.split(" ",1)[1]
        else:
            return None
    
    # ------------------- tokens function -------------------
    def tokens(self, defined):
        linesWithoutTokens = []
        ignoredTokens = []
        
        print("\n------ Token verification ------")
        for line in self.finalLines:
            if("%token" not in line):
                if("IGNORE" in line):
                    tempToks = line.split(" ")[1:]
                    if len(tempToks) > 1:
                        for i in tempToks:
                            ignoredTokens.append(i)
                    else:
                        ignoredTokens.append(tempToks[0])
                else:
                    if("%%" in line):
                        continue
                    linesWithoutTokens.append(line.strip())
        
        undefined = set()   
        alltokens = []
        
        for line in self.finalLines:
            if("%token" in line):
                temporaryLrTokens = line.split(" ")[1:]
                if(len(temporaryLrTokens) > 1):
                    for tok in temporaryLrTokens:
                        if tok not in self.yalpFileTokens:
                            if tok in defined:
                                if tok not in ignoredTokens:
                                    self.yalpFileTokens.append(tok)
                            else:
                                undefined.add(tok)

                        alltokens.append(tok)             
                else:
                    if temporaryLrTokens[0] not in self.yalpFileTokens:
                        if(temporaryLrTokens[0] in defined):
                            if temporaryLrTokens[0] not in ignoredTokens:
                                self.yalpFileTokens.append(temporaryLrTokens[0])
                        else:
                            undefined.add(temporaryLrTokens[0])

                        alltokens.append(temporaryLrTokens[0])           
        
        # repeated tokens checker       
        repeatedTokens = {}
        for tok in alltokens:
            count = alltokens.count(tok)
            if count > 1:
                if tok not in repeatedTokens:
                    repeatedTokens[tok] = count
                
        if undefined:
            print("✘Not all of the Yalp tokens are defined in the Yalex file.\n")
            for el in undefined:
                print(f"!The {el} token is not defined in the Yalex file.")
            print()
        else:
            print("✓Yalp tokens are also in the Yalex file, all of them are defined.\n")

        for k,v in repeatedTokens.items():
            print(f"The {k} token is defined multiple times ({v})")
        
        for tok in ignoredTokens:
            if tok in undefined or tok not in alltokens:
                continue
            else:
                print(f"!The {tok} is IGNORED")   
            
        self.tokensVeri = list(set(alltokens) - undefined)
        return linesWithoutTokens

# name = 'highYalYalp'
# parserInstance = yalpParser(f'src/yalpFiles/{name}.yalp', f'src/identifiedTokens/{name}', name)
# parserInstance.read()
# parserInstance.getGrammarSymbols()
# print("\n------ First Sets ------")
# for symbol in parserInstance.grammarSymbols:
#     first_set = parserInstance.first(symbol)
#     print(f"First({symbol}): {first_set}")

# print("\n------ Following Sets ------")
# for symbol in parserInstance.grammarSymbols:
#     following_set = parserInstance.following(symbol)
#     print(f"Following({symbol}): {following_set}")

# print("\n✓ LR0 automaton & diagram created successfully !\n")