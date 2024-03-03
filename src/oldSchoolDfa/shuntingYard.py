#Copyright (C), 2024-2025, bl33h
#FileName: shuntingYard.py
#Author: Sara Echeverria
#Version: I
#Creation: 02/02/2024
#Last modification: 06/02/2024
# References
# [Sen. (2021). The Shunting Yard Algorithm - Aryak Sen - Medium. Medium. https://medium.com/@aryaks320/the-shunting-yard-algorithm-d2e961965384]

from collections import defaultdict
from graphviz import Digraph
import os

alphabet = [chr(i) for i in range(ord('A'), ord('z') + 1) if i <= ord('Z') or i >= ord('a')] + [str(i) for i in range(10)]
epsilon, kleeneStar, orOperator, concatenationOperator, optionalOperator, plusOperator = 'ε', '*', '|', '·', '?', '+'
openParentheses, closedParentheses = '(', ')'

class regexToAutomaton:
    def __init__(self, symbols=set([])):
        self.states = set()
        self.symbols = symbols    
        self.transitions = defaultdict(defaultdict)
        self.initialState = None
        self.acceptStates = []

    def initialize(self, state):
        self.initialState = state
        self.states.add(state)

    def acceptState(self, state):
        if isinstance(state, int):
            state = [state]
        for s in state:
            if s not in self.acceptStates:
                self.acceptStates.append(s)

    def createTransition(self, fromState, toState, inputSymbol):   
        if isinstance(inputSymbol, str):
            inputSymbol = set([inputSymbol])
        self.states.add(fromState)
        self.states.add(toState)
        if fromState in self.transitions and toState in self.transitions[fromState]:
            self.transitions[fromState][toState] = self.transitions[fromState][toState].union(inputSymbol)
        else:
            self.transitions[fromState][toState] = inputSymbol

    def saveTransitions(self, transitions):  
        for fromState, toStates in transitions.items():
            for state in toStates:
                self.createTransition(fromState, state, toStates[state])

    def updateStates(self, startNum):
        translation = {}
        for i in self.states:
            translation[i] = startNum
            startNum += 1
        # new regexToAutomaton with the same symbols
        updated = regexToAutomaton(self.symbols)  
        updated.initialize(translation[self.initialState])
        # new accept states
        updated.acceptState([translation[s] for s in self.acceptStates])  
        
        for fromState, toStates in self.transitions.items():
            for state in toStates:
                updated.createTransition(translation[fromState], translation[state], toStates[state])
        return [updated, startNum]

    def updateEquivalentStates(self, positions):
        updated = regexToAutomaton(self.symbols)
        for fromState, toStates in self.transitions.items():
            for state in toStates:
                updated.createTransition(positions[fromState], positions[state], toStates[state])
        updated.initialize(positions[self.initialState])
        for s in self.acceptStates:
            updated.acceptState(positions[s])
        return updated

    def epsilonManagement (self, findState):
        allStates = set()
        states = [findState]
        while states:
            state = states.pop()
            allStates.add(state)
            if state in self.transitions:
                for toState in self.transitions[state]:
                    if epsilon in self.transitions[state][toState] and toState not in allStates:
                        states.append(toState)
        return allStates

    def otherTransitions(self, state, symbolKey):
        if isinstance(state, int):
            state = [state]
        transitionStates = set()
        for st in state:
            if st in self.transitions:
                for toState in self.transitions[st]:
                    if symbolKey in self.transitions[st][toState]:
                        transitionStates.add(toState)
        return transitionStates

    def display(self, fileName, projectName):
        # nfaOutput directory exist_ok checker
        outputDir = 'nfaOutput'
        os.makedirs(outputDir, exist_ok=True)
        dotFilePath = os.path.join(outputDir, fileName)
        # create the graph
        graph = Digraph(projectName, filename=fileName, format='png')
        graph.attr(rankdir='LR')
        graph.attr('node', shape='doublecircle')
        for acceptState in self.acceptStates:
            graph.node('s' + str(acceptState))

        graph.attr('node', shape='circle')
        for fromState, toStates in self.transitions.items():
            for toState in toStates:
                label = '|'.join(toStates[toState])
                graph.edge('s' + str(fromState), 's' + str(toState), label=label)

        graph.attr('node', shape='point')
        graph.edge('', 's' + str(self.initialState))
        graph.render(filename=dotFilePath, directory=outputDir, view=False)