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
        self.tree = buildDirectDfa.generateTree()        
        self.tree.getPositions()
        
        # stablish D as the initial state (roots first position) [8.] & accepting states stablishment with # [10.]
        finalSynTree = self.tree.labeledNode(self.tree)
        inState = sorted(finalSynTree[0][1])
        tokenTransitions = [None]
        acceptedStates = []
        initialState = None
        transitions = []
        statesNumber = 1
        rfpStates = []
        names = {}
        
        # rfp states construction
        for i in finalSynTree:
            for j in i:
                if (type(j) == list):
                    j = j.sort()
            
            if (i[0].label == '#'):
                statesNumber = i[4]
        
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
                                    
        # state naming                           
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
                acceptedStates.append(key)
                
        return automatonInfo(initialState, acceptedStates, len(names), finalTransitions, list(names.keys()))

# ------- display the direct dfa media -------
def displayDirectDfa(dfa):
    outputDir = 'directDfaOutput'
    os.makedirs(outputDir, exist_ok=True)
    dotFilePath = os.path.join(outputDir, 'directDfa')
    graph = Digraph('DirectconstructionMethodDFA', filename=dotFilePath, format='png')
    graph.attr(rankdir='LR')

    for state in dfa.states:
        if state == dfa.initialState and state in dfa.acceptedStates:
            graph.node(str(state), shape='doublecircle')
            
        if state == dfa.initialState:
            graph.edge('start', str(state))
            graph.node('start', shape='point')
        elif state in dfa.acceptedStates:
            graph.node(str(state), shape='doublecircle')
        else:
            graph.node(str(state), shape='circle')

    for explicitTransitions in dfa.explicitTransitions:
        origin, explicitSymbols, destiny = explicitTransitions.inState, explicitTransitions.symbol, explicitTransitions.fnState
        graph.edge(str(origin), str(destiny), label=str(explicitSymbols))
        
    graph.render(view=True)

# ------- display the LR0 automaton -------
def displayLR0(dfa, constructionMethod):
    outputDir = 'LR0Output'
    os.makedirs(outputDir, exist_ok=True)
    dotFilePath = os.path.join(outputDir, constructionMethod)
    graph = Digraph('LR0', filename=dotFilePath, format='png')
    graph.attr(rankdir='LR')

    # create a starting point
    graph.node('start', shape='point')
    graph.edge('start', str(dfa.initialState))

    for state in dfa.states:
        # determine the shape of the state node (doublecircle for accepted states)
        shape = 'doublecircle' if state in dfa.acceptedStates else 'circle'
        graph.node(str(state), shape=shape)

    # add edges between nodes
    for explicitTransition in dfa.explicitTransitions:
        origin, explicitSymbol, destiny = explicitTransition.inState, explicitTransition.symbol, explicitTransition.fnState
        graph.edge(str(origin), str(destiny), label=str(explicitSymbol))

    # render the graph to a file and optionally view it
    graph.render(view=True)
    
# ------- display the LR0 diagram -------
def displayLR0Diagram(dfa, constructionMethod, descriptions=None):
    outputDir = 'LR0Output'
    os.makedirs(outputDir, exist_ok=True)
    dotFilePath = os.path.join(outputDir, constructionMethod)
    graph = Digraph('LR0', filename=dotFilePath, format='png')
    graph.attr(rankdir='LR')

    # Create a starting point
    graph.node('start', shape='point')
    graph.edge('start', str(dfa.initialState))

    for state in dfa.states:
        # initialize the label with the state name
        label = f'{state}'

        # check if the state has a description and it's not None
        if descriptions and state in descriptions and descriptions[state] is not None:
            # replace newlines with HTML line breaks for Graphviz
            description = descriptions[state].replace('\n', '<BR/>')
            # append the description to the label
            label += f'<BR/><BR/>{description}'

        # determine the shape of the node
        shape = 'doublecircle' if state in dfa.acceptedStates else 'circle'

        # add the node to the graph with an HTML-like label
        graph.node(str(state), label=f'<{label}>', shape=shape)

    # add edges between nodes
    for transition in dfa.explicitTransitions:
        if transition.symbol is not None:
            origin, symbol, destiny = transition.inState, transition.symbol, transition.fnState
            graph.edge(str(origin), str(destiny), label=str(symbol))

    # render the graph to a file and optionally view it
    graph.render(view=True)