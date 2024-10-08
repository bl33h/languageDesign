# Copyright (C), 2024-2025, bl33h 
# FileName: regexUtilities.py
# Author: Sara Echeverria
# Version: I
# Creation: 06/02/2024
# Last modification: 07/03/2024 

# ------- handles the symbols after the explicit concatenation -------
class explicitSymbols():
    def __init__(self, symbol):
        self.isSpecialChar = False
        self.isFinalSymbol = False
        self.isOperator = False
        self.label = symbol
        self.token = None
    
    # --- set the type of the symbol ---
    # is it an operator?
    def setType(self, isOperator):
        self.isOperator = isOperator
    
    # is it a special character?
    def setSpecialType(self, isSpecial):
        self.isSpecialChar = isSpecial

    # is it a token?
    def setToken(self, newToken):
        self.token = newToken
    
    # is it a final symbol?
    def setFinalSymbol(self, isFinal):
        self.isFinalSymbol = isFinal
    
    def __str__(self):
        if(self.isSpecialChar):
            return repr(self.label).replace("'", "")
        
        return self.label
    
    def __repr__(self):
        return str(self)

# ------- handles the transitions after the explicit concatenation -------
class explicitTransitions():
    def __init__(self, inState, symbol, fnState):
        self.inState = inState
        self.symbol = symbol
        self.fnState = fnState
        
    def __str__(self):
        return f"{self.inState}-{self.symbol}-{self.fnState}"
    
    def __repr__(self):
        return str(self)
    
    def __eq__(self, other):
        if isinstance(other, explicitTransitions):
            return self.inState == other.inState and self.symbol == other.symbol and self.fnState == other.fnState
        return False

# ------- handles the token definitions -------
class defs():
    def __init__(self, name, desc, func=None):
        self.name = name
        self.desc = desc
        self.func = func

    def __str__(self) -> str:
        return f"{self.name}: {self.desc}"

    def __repr__(self):
        return str(self)
    
    def tokensFeatures(self):
        if self.desc == None:
            valDesc = "no description." 
        else:
            if any(s.isSpecialChar == True for s in self.desc):
                tempLD = []
                for i in self.desc:
                    if i.isSpecialChar:
                        tempLD.append(repr(i.label).replace("'", ""))
                    else:
                        tempLD.append(i.label.replace("'", ""))
                valDesc = ''.join(tempLD)
            else:
                tempLD = [s.label for s in self.desc]
                valDesc = ''.join(tempLD)
        
        valFunc = "without function." if self.func is None else self.func
        
        return f"\t- token: {self.name}\n\t   description: {valDesc}\n\t   function: {valFunc}"
    
    def actualCleanDefinition(self):
        if self.desc == None:
            valDesc = "no description." 
        else:
            if any(s.isSpecialChar == True for s in self.desc):
                tempLD = []
                for i in self.desc:
                    if i.isSpecialChar:
                        tempLD.append(repr(i.label).replace("'", ""))
                    else:
                        tempLD.append(i.label.replace("'", ""))
                valDesc = ''.join(tempLD)
            else:
                tempLD = [s.label for s in self.desc]
                valDesc = ''.join(tempLD)
        
        valFunc = "without function." if self.func is None else self.func
        
        return (self.name, valDesc, valFunc)
    
    def __eq__(self, other):
        if isinstance(other, defs):
            return self.name == other.name
        return False  
    
# ------- manages the stack operations for a neat outcome -------
class manageExpression():
    def __init__(self):
        self.manageExpression = []
    
    # get the element at position i
    def getElement(self, i):
        return self.manageExpression[i]
    
    # get the size
    def size(self):
        return len(self.manageExpression)
    
    # empty checker
    def isEmpty(self):
        return True if (self.size() == 0) else False
    
    # push operation
    def push(self, element):
        self.manageExpression.append(element)
    
    # pop operation
    def pop(self):
        return self.manageExpression.pop() if (not self.isEmpty()) else "empty stack." 
    
    # get the last element
    def peek(self):
        return self.manageExpression[-1] if (not self.isEmpty()) else "empty stack." 

# ------- automaton information -------
class automatonInfo():
    def __init__(self, initialState, acceptedStates, numStates, explicitTransitions, states):
        self.explicitTransitions = explicitTransitions
        self.acceptedStates = acceptedStates
        self.initialState = initialState
        self.numStates = numStates
        self.states = states
        self.alphabet = None
    
    def __str__(self):
        return f"- states: {self.states}\n- acceptance states: {self.acceptedStates}"
    
# ------- related to the tokens -------
# get the symbols
def getTransitionSymbols(finalState, transitions):
    acceptedTransitions = []
    transitionSymbols = {}
    
    # get the transitions
    for trans in transitions:
        for lastState in finalState:
            if(trans.fnState == lastState):
                if trans not in acceptedTransitions:
                    acceptedTransitions.append(trans)
    
    # get the symbols
    for trans in acceptedTransitions:
        transitionSymbols[trans.inState] = trans.symbol.label.strip("#")

    return transitionSymbols

# get the final states
def getAcceptanceStates(acceptedStates, transitions):
    acceptedTransitions = []
    acceptanceStates = {}
    
    # get the transitions
    for trans in transitions:
        for lastState in acceptedStates:
            if(trans.fnState == lastState):
                if trans not in acceptedTransitions:
                    acceptedTransitions.append(trans)
    
    # get the final states
    for trans in acceptedTransitions:
        if (trans.fnState not in acceptanceStates):
            acceptanceStates[trans.fnState] = [trans.symbol.label]
        else:
            if (trans.symbol.label not in acceptanceStates[trans.fnState]):
                acceptanceStates[trans.fnState].append(trans.symbol.label)
        
    return acceptanceStates

# get the final states with tokens
def getAcceptanceTokenStates(acceptedStates, transitions):
    acceptanceTokenStates = []
    
    # get the final states
    for trans in transitions:
        for lastState in acceptedStates:
            if(trans.fnState == lastState):
                if trans.inState not in acceptanceTokenStates:
                    acceptanceTokenStates.append(trans.inState)
                    
    acceptedTransitions = []
    acceptanceStates = {}
    
    # get the transitions
    for trans in transitions:
        for lastState in acceptanceTokenStates:
            if(trans.fnState == lastState):
                if trans not in acceptedTransitions:
                    acceptedTransitions.append(trans)
    
    # get the final states with tokens                
    for trans in acceptedTransitions:
        if (trans.fnState not in acceptanceStates):
            acceptanceStates[trans.fnState] = [trans.symbol.label]
        else:
            if (trans.symbol.label not in acceptanceStates[trans.fnState]):
                acceptanceStates[trans.fnState].append(trans.symbol.label)
                    
    return acceptanceStates

# ------- items -------
class itemsInTheProductions():
    def __init__(self, label, completeLabel=None):
        self.label = label
        self.info = completeLabel
        self.terminal = False
        self.dot = False
        
    def setType(self, isTerminal):
        self.terminal = isTerminal
        
    def setFinal(self, isDot):
        self.dot = isDot
    
    def __str__(self):
        return f"{self.label}"
    
    def __repr__(self):
        return str(self)

# ------- actual productions -------
class actualProductions():
    def __init__(self, leftSide, rightSide):
        self.ls = leftSide
        self.rs = rightSide
    
    def __str__(self) -> str:
        return f"{self.ls} → {' '.join([str(s) for s in self.rs])}"
    
    def __repr__(self):
        return str(self)
    
    def __eq__(self, other):
        if not isinstance(other, actualProductions):
            return False
        
        return self.ls == other.ls and self.rs == other.rs

# ------- error management -------
def errorManagement (regex):
    # empty input
    if not regex:
        return (True, "error: no expression found.")

    # balanced parentheses
    openParentheses = 0
    for char in regex:
        if char == '(':
            openParentheses += 1
        elif char == ')':
            openParentheses -= 1
            if openParentheses < 0: 
                return (True, "error: unmatched closing parentheses.")
    
    if openParentheses > 0:
        return (True, "error: unmatched opening parentheses.")
    
    # check for a||b pattern
    if '||' in regex:
        return (True, "error: adjacent OR operators without operand in between.")
    
    return (False, "OK")