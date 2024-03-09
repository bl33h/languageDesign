#Copyright (C), 2024-2025, bl33h 
#FileName: directDfa.py
#Author: Sara Echeverria
#Version: I
#Creation: 06/02/2024
#Last modification: 07/03/2024
# References
# [Urbina. (2022). DFA DIRECTO. Google Docs. https://docs.google.com/presentation/d/1XTelAJ3XDQ49NNDzGuTGTrVueULPrZIT/edit#slide=id.p15]

from directDfa.regexUtilities import *
from directDfa.syntaxTree import *
from graphviz import Digraph
import os

# augmented expression [1.]
def augmentedRegex(expression):
    hashtag = explicitSymbols('#')
    conc = explicitSymbols('.')
    conc.setType(True)
    augmentedExp = expression.copy()
    augmentedExp.append(hashtag)
    augmentedExp.append(conc)
    return augmentedExp

# ------- direct dfa builder -------
class directDfaBuilder():
    def __init__(self, infix, postfix, alphabet):
        self.infix = infix
        self.postfix = postfix
        self.alphabet = alphabet
        hashtag = explicitSymbols('#') 
        conc = explicitSymbols('.') 
        hashtag.setFinalSymbol(True)
        conc.setType(True)
        self.postfix.append(hashtag)
        self.postfix.append(conc)
        self.letterSymbols = {}

    # automaton construction using the syntax tree
    def directDfaFromSynTree(self):
        buildDirectDfa = syntaxTree(self.postfix)
        self.Tree = buildDirectDfa.generateTree()        
        self.Tree.getPositions()
        
        # stablish D as the initial state (roots first position) [8.] & accepting states stablishment with # [10.]
        finalSynTree = self.Tree.labeledNode(self.Tree)
        inState = sorted(finalSynTree[0][1])
        tokenTransitions = [None]
        acceptenceStates = []
        transitions = []
        initialState = None
        statesNumber = 1
        rfpStates = []
        names = {}
        
        rfpStates.append(inState)
        rfpStatesMarked = []
        
        while(not all(t in rfpStatesMarked for t in rfpStates)):
            for t in rfpStates:
                rfpStatesMarked.append(t)
                
                for symbol in self.alphabet:
                    if(symbol == 'ε'):
                        continue
                    U = []

                    for x in t:
                        for el in finalSynTree:
                            if x == el[4] and el[0].label == symbol:
                                for a in el[3]:
                                    if (a not in U):
                                        U.append(a)      
                                                             
                    if (len(U) > 0):
                        if (U not in rfpStates):
                            rfpStates.append(U)

                    if(t != []):
                        if(U != []):
                            for el in finalSynTree:
                                if (el[0].label == symbol):
                                    if (symbol == '#'):
                                        if (el[0].token not in tokenTransitions):
                                            tokenTransitions.append(el[0].token)
                                            transitions.append(explicitTransitions(t, el[0], U)) 
                                            break 
                                    else:
                                        transitions.append(explicitTransitions(t, el[0], U))
                                        break
                                    
        
        for newState in rfpStatesMarked:
            if(newState != []):
                name = 's' + str(len(names))
                names[name] = newState

        # transition table construction [9.]
        finalTransitions = []

        for t in transitions:     
            newInState = None
            newFnState = None
            for key, value in names.items():
                if(value == t.inState):
                    newInState = key
                if(value == t.fnState):
                    newFnState = key     
            finalTransitions.append(explicitTransitions(str(newInState), t.symbol, str(newFnState)))
              
        for key, values in names.items():
            if inState in values or inState == values:
                initialState = key
            
            if statesNumber in values:
                acceptenceStates.append(key)
                
        return automatonInfo(initialState, acceptenceStates, len(names), finalTransitions, list(names.keys()))

# ------- display the direct dfa media -------
def displayDirectDfa(dfa):
    outputDir = 'directDfaOutput'
    os.makedirs(outputDir, exist_ok=True)
    dotFilePath = os.path.join(outputDir, 'directDfa')
    graph = Digraph('DirectMethodDFA', filename=dotFilePath, format='png')
    graph.attr(rankdir='LR')

    for state in dfa.states:
        if state == dfa.initialState and state in dfa.acceptenceStates:
            graph.node(str(state), shape='doublecircle')
            
        if state == dfa.initialState:
            graph.edge('start', str(state))
            graph.node('start', shape='point')
        elif state in dfa.acceptenceStates:
            graph.node(str(state), shape='doublecircle')
        else:
            graph.node(str(state), shape='circle')

    for explicitTransitions in dfa.explicitTransitions:
        origin, explicitSymbols, destiny = explicitTransitions.inState, explicitTransitions.symbol, explicitTransitions.fnState
        graph.edge(str(origin), str(destiny), label=str(explicitSymbols))
        
    graph.render()