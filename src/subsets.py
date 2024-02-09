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
        # mapping DFA state to an index
        self.dfaStates[self.dfaStartState] = 0  

        while queue:
            currentDfaState = queue.pop(0)
            for symbol in self.nfa.symbols:
                if symbol != epsilon:
                    nextState = self.epsilonClosure(self.move(currentDfaState, symbol))
                    if nextState not in self.dfaStates:
                        self.dfaStates[nextState] = len(self.dfaStates)
                        queue.append(nextState)
                    self.dfaTransitions[currentDfaState][symbol].add(nextState)
                    if any(s in self.nfa.acceptStates for s in nextState):
                        self.dfaAcceptedStates.append(nextState)
    
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
        states = list(self.dfaStates.keys())
        equivalentStates = {}
        # non-final and final states groups
        equivalentGroups = [set(), set()] 

        # equivalent groups based on accepting and non-accepting states
        for st in states:
            if st in self.dfaAcceptedStates:
                equivalentGroups[1].add(st)
            else:
                equivalentGroups[0].add(st)

        # distinguishable states identifier
        def distinguishable(state1, state2):
            for symbol in self.nfa.symbols:
                nextState1 = next(iter(self.dfaTransitions[state1][symbol]), None)
                nextState2 = next(iter(self.dfaTransitions[state2][symbol]), None)
                if nextState1 != nextState2:
                    return True
            return False

        currentGroup = 2 
        while currentGroup < len(equivalentGroups):
            # new groups for the next iteration
            newGroups = [set(), set()]  
            for st in equivalentGroups[currentGroup]:
                distinguished = False
                for stEq in equivalentGroups[currentGroup - 1]:
                    if distinguishable(st, stEq):
                        distinguished = True
                        break
                if distinguished:
                    newGroups[0].add(st)
                else:
                    newGroups[1].add(st)
            # remove the current group and add the new groups
            equivalentGroups.pop(currentGroup)  
            equivalentGroups.extend(newGroups)
            currentGroup += 1

        # equivalent states dictionary update
        for i, group in enumerate(equivalentGroups):
            for state in group:
                equivalentStates[state] = i

        # equivalent states minimization
        minDfaStates = {}
        minDfaTransitions = defaultdict(lambda: defaultdict(set))
        minDfaAcceptedStates = set()

        for state, groupIndex in equivalentStates.items():
            minDfaStates[groupIndex] = state
            if state in self.dfaAcceptedStates:
                minDfaAcceptedStates.add(groupIndex)
            for symbol, transitions in self.dfaTransitions[state].items():
                nextState = next(iter(transitions), None)
                if nextState:
                    followingGroup = equivalentStates[nextState]
                    minDfaTransitions[groupIndex][symbol].add(followingGroup)

        # attributes update
        self.dfaStates = minDfaStates
        self.dfaTransitions = minDfaTransitions
        self.dfaAcceptedStates = minDfaAcceptedStates
        
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