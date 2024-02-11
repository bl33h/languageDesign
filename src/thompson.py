#Copyright (C), 2024-2025, bl33h 
#FileName: regexToAutomaton.py
#Author: Sara Echeverria 
#Version: I
#Creation: 11/02/2024
#Last modification: 07/02/2024
# References
# [Attaching NFA Fragments together (regexToAutomaton). (n.d.). Stack Overflow. https://stackoverflow.com/questions/50916898/attaching-nfa-fragments-together-regexToAutomaton]
# [automata-toolkit. (2021). PyPI. https://pypi.org/project/automata-toolkit/]
# [Martinez. (2023). Automata: An alternative NFA is generated by regexToAutomaton's Algorithm for Construction. CopyProgramming. https://copyprogramming.com/howto/regexToAutomaton-s-construction-algorithm-produces-a-different-nfa]

from collections import defaultdict
from graphviz import Digraph
import os

alphabet = [chr(i) for i in range(ord('A'), ord('z') + 1) if i <= ord('Z') or i >= ord('a')] + [str(i) for i in range(10)]
epsilon, kleeneStar, orOperator, concatenationOperator, optionalOperator, plusOperator = 'ε', '*', '|', '·', '?', '+'
openParentheses, closedParentheses = '(', ')'

# ------- main method -------
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

# ------- mcnaughton yamada thompson method to convert regex to nfa -------     
class thompson:
    def __init__(self, regex):
        self.regex = regex
        self.createNFA()

    def comparePrecedence(op):
        if op == orOperator:
            return 1
        elif op == concatenationOperator:
            return 2
        elif op == kleeneStar:
            return 3
        elif op == optionalOperator:
            return 3
        elif op == plusOperator:
            return 3
        else:       
            return 0

    def handleSymbol(inputSymbol):   
        initialState = 1
        nextState = 2
        basicregexToAutomaton = regexToAutomaton(set([inputSymbol]))
        basicregexToAutomaton.initialize(initialState)
        basicregexToAutomaton.acceptState(nextState)
        basicregexToAutomaton.createTransition(initialState, nextState, inputSymbol)
        return basicregexToAutomaton

    def handleOpt(self, a):
        [a, m1] = a.updateStates(2)
        initialState = 1
        nextState = m1
        optionalRegexToAutomaton = regexToAutomaton(a.symbols)
        optionalRegexToAutomaton.initialize(initialState)
        optionalRegexToAutomaton.acceptState(nextState)
        
        # create an epsilon transition from the initial state to the new accept state to make the element optional
        optionalRegexToAutomaton.createTransition(initialState, a.initialState, epsilon)
        optionalRegexToAutomaton.createTransition(a.acceptStates[0], nextState, epsilon)
        optionalRegexToAutomaton.createTransition(initialState, nextState, epsilon)
        optionalRegexToAutomaton.saveTransitions(a.transitions)
        
        return optionalRegexToAutomaton
        
    def handlePlus(self, a):
        # Update the states of automaton 'a' to ensure there's no overlap with the new states we're going to add
        [a, m1] = a.updateStates(2)
        
        # Initialize the new automaton for handling '+'
        initialState = 1  # This will be the new initial state
        nextState = m1    # This will be the new accept state, ensuring we have moved beyond all states in 'a'
        
        plusAutomaton = regexToAutomaton(a.symbols)
        plusAutomaton.initialize(initialState)
        plusAutomaton.acceptState(nextState)
        
        # Create an epsilon transition from the new initial state to the initial state of 'a'
        plusAutomaton.createTransition(initialState, a.initialState, epsilon)
        
        # For every accept state of 'a', create two transitions:
        # 1. An epsilon transition back to the initial state of 'a' to allow for repeated occurrences
        # 2. An epsilon transition to the new accept state to allow for the sequence to end
        for acceptState in a.acceptStates:
            plusAutomaton.createTransition(acceptState, a.initialState, epsilon)
            plusAutomaton.createTransition(acceptState, nextState, epsilon)
        
        # Include the transitions from 'a' into the new automaton
        plusAutomaton.saveTransitions(a.transitions)

        return plusAutomaton


    def handleUnion(a, b):   
        [a, m1] = a.updateStates(2)
        [b, m2] = b.updateStates(m1)
        initialState = 1
        nextState = m2
        unionregexToAutomaton = regexToAutomaton(a.symbols.union(b.symbols))
        unionregexToAutomaton.initialize(initialState)
        unionregexToAutomaton.acceptState(nextState)
        unionregexToAutomaton.createTransition(unionregexToAutomaton.initialState, a.initialState, epsilon)
        unionregexToAutomaton.createTransition(unionregexToAutomaton.initialState, b.initialState, epsilon)
        unionregexToAutomaton.createTransition(a.acceptStates[0], unionregexToAutomaton.acceptStates[0], epsilon)
        unionregexToAutomaton.createTransition(b.acceptStates[0], unionregexToAutomaton.acceptStates[0], epsilon)
        unionregexToAutomaton.saveTransitions(a.transitions)
        unionregexToAutomaton.saveTransitions(b.transitions)
        return unionregexToAutomaton

    def handleConcatenation(a, b):    
        [a, m1] = a.updateStates(1)
        [b, m2] = b.updateStates(m1)
        initialState = 1
        nextState = m2 - 1
        concatenationregexToAutomaton = regexToAutomaton(a.symbols.union(b.symbols))
        concatenationregexToAutomaton.initialize(initialState)
        concatenationregexToAutomaton.acceptState(nextState)
        concatenationregexToAutomaton.createTransition(a.acceptStates[0], b.initialState, epsilon)
        concatenationregexToAutomaton.saveTransitions(a.transitions)
        concatenationregexToAutomaton.saveTransitions(b.transitions)
        return concatenationregexToAutomaton

    def handleKleeneStar(a):  
        [a, m1] = a.updateStates(2)
        initialState = 1
        nextState = m1
        kleeneregexToAutomaton = regexToAutomaton(a.symbols)
        kleeneregexToAutomaton.initialize(initialState)
        kleeneregexToAutomaton.acceptState(nextState)
        kleeneregexToAutomaton.createTransition(kleeneregexToAutomaton.initialState, a.initialState, epsilon)
        kleeneregexToAutomaton.createTransition(kleeneregexToAutomaton.initialState, kleeneregexToAutomaton.acceptStates[0], epsilon)
        kleeneregexToAutomaton.createTransition(a.acceptStates[0], kleeneregexToAutomaton.acceptStates[0], epsilon)
        kleeneregexToAutomaton.createTransition(a.acceptStates[0], a.initialState, epsilon)
        kleeneregexToAutomaton.saveTransitions(a.transitions)
        return kleeneregexToAutomaton

    def createNFA(self):
        temp = ''
        prev = ''
        symbols = set()
        # process the regex
        for ch in self.regex:
            if ch in alphabet:
                symbols.add(ch)
            if ch in alphabet or ch == openParentheses:
                if prev != concatenationOperator and (prev in alphabet or prev in [kleeneStar, closedParentheses]): 
                    temp += concatenationOperator
            temp += ch
            prev = ch
        self.regex = temp
        temp = ''
        stack = []
        for ch in self.regex:
            if ch in alphabet:
                temp += ch 
            elif ch == openParentheses:
                stack.append(ch) 
            elif ch == closedParentheses:
                while stack[-1] != openParentheses:
                    temp += stack.pop()
                stack.pop()    
            else:
                while stack and thompson.comparePrecedence(stack[-1]) >= thompson.comparePrecedence(ch):
                    temp += stack.pop()
                stack.append(ch) 
        while stack:
            temp += stack.pop() 
        self.regex = temp

        # build NFA
        self.regexToAutomatonStack = []
        for ch in self.regex:
            if ch in alphabet:
                self.regexToAutomatonStack.append(thompson.handleSymbol(ch)) 
            elif ch == orOperator:
                b = self.regexToAutomatonStack.pop()
                a = self.regexToAutomatonStack.pop()
                self.regexToAutomatonStack.append(thompson.handleUnion(a, b)) 
            elif ch == concatenationOperator:
                b = self.regexToAutomatonStack.pop()
                a = self.regexToAutomatonStack.pop()
                self.regexToAutomatonStack.append(thompson.handleConcatenation(a, b))
            elif ch == kleeneStar:
                a = self.regexToAutomatonStack.pop()
                self.regexToAutomatonStack.append(thompson.handleKleeneStar(a))
            elif ch == optionalOperator:
                a = self.regexToAutomatonStack.pop()
                self.regexToAutomatonStack.append(self.handleOpt(a))
            elif ch == plusOperator:
                a = self.regexToAutomatonStack.pop()
                self.regexToAutomatonStack.append(self.handlePlus(a))
        self.nfa = self.regexToAutomatonStack.pop()
        self.nfa.symbols = symbols

    def analyzeNFA(self, string):
        print('\n------------\nNFA simulation')
        string = string.replace('@', epsilon)
        currentState = self.nfa.initialState
        currentState = self.nfa.epsilonManagement(currentState)

        for ch in string:
            if ch == epsilon:
                continue
            states = self.nfa.otherTransitions(currentState, ch)
            print(f"closure states: {states}, input symbol: {ch}, next state: {states}")
            currentState = set()
            for s in states:
                currentState = currentState.union(self.nfa.epsilonManagement(s))
            print(f"closure states: {currentState}, input symbol: {epsilon}, next state: {currentState}")
        if currentState.intersection(self.nfa.acceptStates):
            print(f"\nstring '{string}' accepted.")
        else:
            print(f"\nstring '{string}' not accepted, stops at state {currentState}.")
        return currentState.intersection(self.nfa.acceptStates)

    def displayNFA(self):
        self.nfa.display('nfa.gv', 'nondeterministicFiniteStateMachine')