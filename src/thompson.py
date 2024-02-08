#Copyright (C), 2024-2025, bl33h
#FileName: thompson.py
#Author: Sara Echeverria
#Version: I
#Creation: 06/02/2024
#Last modification: 06/02/2024

from shuntingYard import shuntingYard
from collections import defaultdict
from graphviz import Digraph
import os

alphabet = [chr(i) for i in range(ord('A'), ord('z') + 1) if i <= ord('Z') or i >= ord('a')] + [str(i) for i in range(10)]
epsilon, kleeneStar, unionOperator, concatenationOperator = 'ε', '*', '|', '·'
openParenthesis, closeParenthesis = '(', ')'

class Thompson:
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
        # new Thompson with the same symbols
        updated = Thompson(self.symbols)  
        updated.initialize(translation[self.initialState])
        # new accept states
        updated.acceptState([translation[s] for s in self.acceptStates])  
        
        for fromState, toStates in self.transitions.items():
            for state in toStates:
                updated.createTransition(translation[fromState], translation[state], toStates[state])
        return [updated, startNum]

    def updateEquivalentStates(self, positions):
        updated = Thompson(self.symbols)
        for fromState, toStates in self.transitions.items():
            for state in toStates:
                updated.createTransition(positions[fromState], positions[state], toStates[state])
        updated.initialize(positions[self.initialState])
        for s in self.acceptStates:
            updated.acceptState(positions[s])
        return updated

    def epsilonClosure(self, findState):
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
        # nfaOutput directory exists checker
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
        
class NFA:
    def __init__(self, regex):
        self.regex = regex
        self.createNFA()

    def comparePrecedence(op):
        if op == unionOperator:
            return 1
        elif op == concatenationOperator:
            return 2
        elif op == kleeneStar:
            return 3
        else:       
            return 0

    def handleSymbol(inputSymbol):   
        initialState = 1
        nextState = 2
        basicThompson = Thompson(set([inputSymbol]))
        basicThompson.initialize(initialState)
        basicThompson.acceptState(nextState)
        basicThompson.createTransition(initialState, nextState, inputSymbol)
        return basicThompson

    def handleUnion(a, b):   
        [a, m1] = a.updateStates(2)
        [b, m2] = b.updateStates(m1)
        initialState = 1
        nextState = m2
        unionThompson = Thompson(a.symbols.union(b.symbols))
        unionThompson.initialize(initialState)
        unionThompson.acceptState(nextState)
        unionThompson.createTransition(unionThompson.initialState, a.initialState, epsilon)
        unionThompson.createTransition(unionThompson.initialState, b.initialState, epsilon)
        unionThompson.createTransition(a.acceptStates[0], unionThompson.acceptStates[0], epsilon)
        unionThompson.createTransition(b.acceptStates[0], unionThompson.acceptStates[0], epsilon)
        unionThompson.saveTransitions(a.transitions)
        unionThompson.saveTransitions(b.transitions)
        return unionThompson

    def handleConcatenation(a, b):    
        [a, m1] = a.updateStates(1)
        [b, m2] = b.updateStates(m1)
        initialState = 1
        nextState = m2 - 1
        concatenationThompson = Thompson(a.symbols.union(b.symbols))
        concatenationThompson.initialize(initialState)
        concatenationThompson.acceptState(nextState)
        concatenationThompson.createTransition(a.acceptStates[0], b.initialState, epsilon)
        concatenationThompson.saveTransitions(a.transitions)
        concatenationThompson.saveTransitions(b.transitions)
        return concatenationThompson

    def handleKleeneStar(a):  
        [a, m1] = a.updateStates(2)
        initialState = 1
        nextState = m1
        kleeneThompson = Thompson(a.symbols)
        kleeneThompson.initialize(initialState)
        kleeneThompson.acceptState(nextState)
        kleeneThompson.createTransition(kleeneThompson.initialState, a.initialState, epsilon)
        kleeneThompson.createTransition(kleeneThompson.initialState, kleeneThompson.acceptStates[0], epsilon)
        kleeneThompson.createTransition(a.acceptStates[0], kleeneThompson.acceptStates[0], epsilon)
        kleeneThompson.createTransition(a.acceptStates[0], a.initialState, epsilon)
        kleeneThompson.saveTransitions(a.transitions)
        return kleeneThompson

    def createNFA(self):
        temp = ''
        prev = ''
        symbols = set()
        # process the regex
        for ch in self.regex:
            if ch in alphabet:
                symbols.add(ch)
            if ch in alphabet or ch == openParenthesis:
                if prev != concatenationOperator and (prev in alphabet or prev in [kleeneStar, closeParenthesis]): 
                    temp += concatenationOperator
            temp += ch
            prev = ch
        self.regex = temp
        temp = ''
        stack = []
        for ch in self.regex:
            if ch in alphabet:
                temp += ch 
            elif ch == openParenthesis:
                stack.append(ch) 
            elif ch == closeParenthesis:
                while stack[-1] != openParenthesis:
                    temp += stack.pop()
                stack.pop()    
            else:
                while stack and NFA.comparePrecedence(stack[-1]) >= NFA.comparePrecedence(ch):
                    temp += stack.pop()
                stack.append(ch) 
        while stack:
            temp += stack.pop() 
        self.regex = temp

        # build NFA
        self.ThompsonStack = []
        for ch in self.regex:
            if ch in alphabet:
                self.ThompsonStack.append(NFA.handleSymbol(ch)) 
            elif ch == unionOperator:
                b = self.ThompsonStack.pop()
                a = self.ThompsonStack.pop()
                self.ThompsonStack.append(NFA.handleUnion(a, b)) 
            elif ch == concatenationOperator:
                b = self.ThompsonStack.pop()
                a = self.ThompsonStack.pop()
                self.ThompsonStack.append(NFA.handleConcatenation(a, b))
            elif ch == kleeneStar:
                a = self.ThompsonStack.pop()
                self.ThompsonStack.append(NFA.handleKleeneStar(a))
        self.nfa = self.ThompsonStack.pop()
        self.nfa.symbols = symbols

    def analyzeNFA(self, string):
        print('\n------------\nNFA simulation')
        string = string.replace('@', epsilon)
        currentState = self.nfa.initialState
        currentState = self.nfa.epsilonClosure(currentState)

        for ch in string:
            if ch == epsilon:
                continue
            states = self.nfa.otherTransitions(currentState, ch)
            print(f"closure states: {states}, input symbol: {ch}, next state: {states}")
            currentState = set()
            for s in states:
                currentState = currentState.union(self.nfa.epsilonClosure(s))
            print(f"closure states: {currentState}, input symbol: {epsilon}, next state: {currentState}")
        if currentState.intersection(self.nfa.acceptStates):
            print(f"\nstring '{string}' accepted.")
        else:
            print(f"\nstring '{string}' not accepted, stops at state {currentState}.")
        return currentState.intersection(self.nfa.acceptStates)

    def displayNFA(self):
        self.nfa.display('nfa.gv', 'nondeterministic_finite_state_machine')

if __name__ == "__main__":
    regex_input = input("enter the regular expression: ")
    postfix = shuntingYard(regex_input)
    nfa = NFA(postfix)
    nfa.displayNFA()
    string_w = input("enter the string w: ")
    if nfa.analyzeNFA(string_w):
        print(f"the string'{string_w}' w∈L(r)")
    else:
        print(f"the string'{string_w}' w∉L(r)")