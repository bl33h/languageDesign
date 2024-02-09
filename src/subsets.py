#Copyright (C), 2024-2025, bl33h
#FileName: subsets.py
#Author: Sara Echeverria
#Version: I
#Creation: 07/02/2024
#Last modification: 09/02/2024
# References
# GeeksforGeeks. (2022). Converting Epsilon NFA to DFA using Python and Graphviz. https://www.geeksforgeeks.org/converting-epsilon-nfa-to-dfa-using-python-and-graphviz/

from collections import defaultdict
from graphviz import Digraph
from thompson import *
from shuntingYard import *

# dfa convertion using the nfa output from thompson
class dfaFromNfa:
    def __init__(self, nfa):
        self.nfa = nfa
        self.dfaStates = {}
        self.dfaStartState = None
        self.dfaAcceptedStates = []
        self.dfaTransitions = defaultdict(lambda: defaultdict(set))
        self.constructDfa()

    def epsilonClosure(self, states):
        closure = set(states)
        stack = list(states)
        while stack:
            state = stack.pop()
            if state in self.nfa.transitions:
                for toState in self.nfa.transitions[state]:
                    if epsilon in self.nfa.transitions[state][toState] and toState not in closure:
                        closure.add(toState)
                        stack.append(toState)
        return frozenset(closure)

    def move(self, states, symbol):
        nextStates = set()
        for state in states:
            if state in self.nfa.transitions:
                for toState, symbols in self.nfa.transitions[state].items():
                    if symbol in symbols:
                        nextStates.add(toState)
        return frozenset(nextStates)

    def constructDfa(self):
        self.dfaStartState = self.epsilonClosure([self.nfa.initialState])
        queue = [self.dfaStartState]
        visited = set()
        self.dfaStates[self.dfaStartState] = 0

        while queue:
            currentDfaState = queue.pop(0)
            visited.add(currentDfaState)

            for symbol in self.nfa.symbols:
                if symbol != epsilon:
                    nextState = self.epsilonClosure(self.move(currentDfaState, symbol))
                    if nextState and nextState not in self.dfaStates:  
                        # nextState is not empty and new checker
                        self.dfaStates[nextState] = len(self.dfaStates)
                        queue.append(nextState)
                    # transitions record for existing states
                    if nextState:  
                        self.dfaTransitions[currentDfaState][symbol].add(nextState)
                    if any(s in self.nfa.acceptStates for s in nextState) and nextState not in self.dfaAcceptedStates:
                        self.dfaAcceptedStates.append(nextState)
        self.dfaAcceptedStates = [state for state in self.dfaStates.keys() if any(s in self.nfa.acceptStates for s in state)]
    
    def simulateDFA(self, inputString):
        print('\n------------\nDFA simulation')
        currentState = self.dfaStartState
        print(f"closure: {currentState}")

        for symbol in inputString:
            print(f"input symbol: {symbol}, current state: {currentState}")
            if symbol in self.nfa.symbols and symbol != epsilon:
                nextState = next(iter(self.dfaTransitions[currentState][symbol]), None)
                if nextState:
                    print(f"transition state: {nextState}")
                    currentState = nextState
                else:
                    print("no transition found. string rejected.")
                    return False
            else:
                print("symbol not in DFA alphabet. string rejected.")
                return False
            
        # current state is an accept state checker
        isAccepted = currentState in self.dfaAcceptedStates
        print(f"final state: {currentState}.")
        print(f"\nstring {'accepted' if isAccepted else 'rejected'}.")
        return isAccepted
    
    def displayDFA(self, fileName='dfa.gv', projectName='deterministicFiniteStateMachine'):
        outputDir = 'dfaOutput'
        os.makedirs(outputDir, exist_ok=True)
        dotFilePath = os.path.join(outputDir, fileName)
        graph = Digraph(projectName, filename=fileName, format='png')
        graph.attr(rankdir='LR')
        graph.attr('node', shape='doublecircle')
        for acceptState in self.dfaAcceptedStates:
            graph.node('s' + str(self.dfaStates[acceptState]))

        graph.attr('node', shape='circle')
        for fromState, transitions in self.dfaTransitions.items():
            for symbol, toStates in transitions.items():
                for toState in toStates:
                    graph.edge('s' + str(self.dfaStates[fromState]), 's' + str(self.dfaStates[toState]), label=symbol)

        graph.attr('node', shape='point')
        graph.edge('', 's' + str(self.dfaStates[self.dfaStartState]))
        graph.render(filename=dotFilePath, directory=outputDir, view=False)
    
    # minimize the dfa output
    def minimize(self):
        # accepting and non-accepting states
        partition = [set(filter(lambda s: s in self.dfaAcceptedStates, self.dfaStates.keys())),
                    set(filter(lambda s: s not in self.dfaAcceptedStates, self.dfaStates.keys()))]

        newPartition = []
        while partition != newPartition:
            if newPartition:
                partition = newPartition
            newPartition = []
            for p in partition:
                subsets = self.refinePartition(p, partition)
                newPartition.extend(subsets)

        # states and transitions based on the new partition update
        self.statesTransitionsUpdate(newPartition)

    def refinePartition(self, group, partition):
        newRefGroups = []
        for symbol in self.nfa.symbols:
            if symbol == epsilon:
                continue
            symbolGroups = defaultdict(set)
            for state in group:
                for p in partition:
                    if any(followingState in p for followingState in self.move({state}, symbol)):
                        symbolGroups[frozenset(p)].add(state)
                        break
            newRefGroups.extend(symbolGroups.values())
        return newRefGroups if newRefGroups else [group]
    
    def statesTransitionsUpdate(self, partition):
        newTransitions = defaultdict(lambda: defaultdict(set))
        newAcceptedStates = set()

        for idx, group in enumerate(partition):
                self.dfaStartState = idx
                break

        for group in partition:
            for state in group:
                if state in self.dfaAcceptedStates:
                    newAcceptedStates.add(frozenset(group))
                for symbol, nextStates in self.dfaTransitions[state].items():
                    for nextState in nextStates:
                        for p in partition:
                            if nextState in p:
                                newTransitions[frozenset(group)][symbol].add(frozenset(p))
                                break

        # state mappings to use the new partition index update
        self.dfaStates = {frozenset(group): idx for idx, group in enumerate(partition)}
        self.dfaTransitions = {self.dfaStates[group]: {symbol: {self.dfaStates[ns] for ns in nextStates} for symbol, nextStates in transitions.items()} for group, transitions in newTransitions.items()}
        self.dfaAcceptedStates = [self.dfaStates[group] for group in newAcceptedStates]

    def simulateMinimizedDFA(self, inputString):
        print('\n------------\nminimized DFA simulation')
        currentState = self.dfaStartState
        print(f"closure: {currentState}")

        for symbol in inputString:
            print(f"input symbol: {symbol}, current state: {currentState}")
            if symbol in self.nfa.symbols: 
                nextStateGroup = next(iter(self.dfaTransitions[currentState].get(symbol, set())), None)
                if nextStateGroup is not None:
                    print(f"transition state: {nextStateGroup}")
                    currentState = nextStateGroup
                else:
                    print("no transition found for this symbol. string rejected.")
                    return False
            else:
                print("symbol not in DFA alphabet. string rejected.")
                return False

        # current state accept state checker
        isAccepted = currentState in self.dfaAcceptedStates
        print(f"final state: {currentState}.")
        print(f"\nstring {'accepted' if isAccepted else 'rejected'}.")
        return isAccepted
        
    def displayMinimizedDFA(self, fileName='minimizedDfa.gv', projectName='minimizedDeterministicFiniteStateMachine'):
        outputDir = 'minDfaOutput'
        os.makedirs(outputDir, exist_ok=True)
        dotFilePath = os.path.join(outputDir, fileName)
        graph = Digraph(projectName, filename=fileName, format='png')
        graph.attr(rankdir='LR')
        graph.attr('node', shape='doublecircle')

        for acceptState in self.dfaAcceptedStates:
            graph.node('s' + str(acceptState))

        graph.attr('node', shape='circle')

        for fromState, transitions in self.dfaTransitions.items():
            for symbol, toStates in transitions.items():
                for toState in toStates:
                    graph.edge('s' + str(fromState), 's' + str(toState), label=symbol)

        graph.attr('node', shape='point')
        graph.edge('', 's' + str(self.dfaStartState))
        graph.render(filename=dotFilePath, directory=outputDir, view=False)