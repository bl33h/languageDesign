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
from oldSchoolDfa.thompson import *
from oldSchoolDfa.shuntingYard import *

# ------- dfa convertion using the nfa output from thompson -------
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
    
    # ------- minimize the dfa output -------
    def minimize(self):
        partition = [set(filter(lambda s: s not in self.dfaAcceptedStates, self.dfaStates.keys())),
                    set(self.dfaAcceptedStates)]

        def find_partition(state, partition):
            for block in partition:
                if state in block:
                    return block
            return None

        while True:
            new_partition = []
            for block in partition:
                block_partition = {}
                for state in block:
                    key = frozenset(
                        (symbol, frozenset(find_partition(next(iter(self.dfaTransitions[state].get(symbol, set())), None), partition) or []))
                        for symbol in self.nfa.symbols if symbol != epsilon
                    )
                    if key in block_partition:
                        block_partition[key].add(state)
                    else:
                        block_partition[key] = {state}
                new_partition.extend(list(block_partition.values()))

            if set(map(frozenset, new_partition)) == set(map(frozenset, partition)):
                break
            partition = new_partition

        new_states = {}
        new_transitions = defaultdict(lambda: defaultdict(set))
        new_accepted_states = []

        for i, block in enumerate(partition):
            new_state_id = frozenset(block)
            for state in block:
                new_states[state] = i
                if state in self.dfaAcceptedStates:
                    new_accepted_states.append(i)
                    break

        for block in partition:
            representative = next(iter(block))
            for symbol in self.nfa.symbols:
                if symbol != epsilon:
                    target_state = next(iter(self.dfaTransitions[representative].get(symbol, set())), None)
                    if target_state is not None:
                        for p_block in partition:
                            if target_state in p_block:
                                new_transitions[new_states[representative]][symbol].add(new_states[next(iter(p_block))])
                                break

        self.dfaStates = {frozenset(block): i for i, block in enumerate(partition)}
        self.dfaTransitions = new_transitions
        self.dfaAcceptedStates = list(set(new_accepted_states))
        self.dfaStartState = new_states[self.dfaStartState]

    def refinePartition(self, group, partition):
        newRefGroups = defaultdict(set)
        for state in group:
            for symbol in self.nfa.symbols:
                if symbol == epsilon:
                    continue
                found = False
                for p in partition:
                    if any(nextState in p for nextState in self.move({state}, symbol)):
                        newRefGroups[p].add(state)
                        found = True
                        break
                if not found:
                    newRefGroups[frozenset()].add(state)
        return list(newRefGroups.values()) if newRefGroups else [group]

    def statesTransitionsUpdate(self, partition):
        newStateIndex = 0
        newStates = {}
        newAcceptedStates = set()
        newTransitions = defaultdict(lambda: defaultdict(set))

        # Assigning new state indices
        for group in partition:
            newStates[frozenset(group)] = newStateIndex
            if any(state in self.dfaAcceptedStates for state in group):
                newAcceptedStates.add(newStateIndex)
            newStateIndex += 1

        # Rebuilding transitions for the new states
        for group in partition:
            newState = newStates[frozenset(group)]
            for state in group:
                for symbol, toStates in self.dfaTransitions[state].items():
                    for toState in toStates:
                        newToState = [newStates[frozenset(p)] for p in partition if toState in p][0]
                        newTransitions[newState][symbol].add(newToState)

        self.dfaStates = {frozenset(group): i for i, group in enumerate(partition)}
        self.dfaTransitions = newTransitions
        self.dfaAcceptedStates = list(newAcceptedStates)

        # Updating the start state for the minimized DFA
        for group in partition:
            if self.dfaStartState in group:
                self.dfaStartState = newStates[frozenset(group)]
                break
    
    # ------- simulation and graphic display -------        
    def simulateMinimizedDFA(self, inputString):
        print('\n------------\nminimized DFA simulation')
        currentState = self.dfaStartState
        print(f"Start state: {currentState}")

        for symbol in inputString:
            print(f"input symbol: {symbol}, current state: {currentState}")
            nextState = next(iter(self.dfaTransitions[currentState].get(symbol, set())), None)
            if nextState is not None:
                print(f"transition state: {nextState}")
                currentState = nextState
            else:
                print("no transition found for this symbol. string rejected.")
                return False

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