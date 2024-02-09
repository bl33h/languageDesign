#Copyright (C), 2024-2025, bl33h
#FileName: subsets.py
#Author: Sara Echeverria
#Version: I
#Creation: 07/02/2024
#Last modification: 08/02/2024

from collections import defaultdict
from graphviz import Digraph
from thompson import *
from shuntingYard import *

class DFAFromNFA:
    def __init__(self, nfa):
        self.nfa = nfa
        self.dfa_states = {}
        self.dfa_start_state = None
        self.dfa_accept_states = []
        self.dfa_transitions = defaultdict(lambda: defaultdict(set))
        self.constructDfa()

    def epsilonClosure(self, states):
        closure = set(states)
        stack = list(states)
        while stack:
            state = stack.pop()
            if state in self.nfa.transitions:
                for to_state in self.nfa.transitions[state]:
                    if epsilon in self.nfa.transitions[state][to_state] and to_state not in closure:
                        closure.add(to_state)
                        stack.append(to_state)
        return frozenset(closure)

    def move(self, states, symbol):
        next_states = set()
        for state in states:
            if state in self.nfa.transitions:
                for to_state, symbols in self.nfa.transitions[state].items():
                    if symbol in symbols:
                        next_states.add(to_state)
        return frozenset(next_states)

    def constructDfa(self):
        self.dfa_start_state = self.epsilonClosure([self.nfa.initialState])
        queue = [self.dfa_start_state]
        self.dfa_states[self.dfa_start_state] = 0  # Mapping DFA state to an index

        while queue:
            current_dfa_state = queue.pop(0)
            for symbol in self.nfa.symbols:
                if symbol != epsilon:
                    next_state = self.epsilonClosure(self.move(current_dfa_state, symbol))
                    if next_state not in self.dfa_states:
                        self.dfa_states[next_state] = len(self.dfa_states)
                        queue.append(next_state)
                    self.dfa_transitions[current_dfa_state][symbol].add(next_state)
                    if any(s in self.nfa.acceptStates for s in next_state):
                        self.dfa_accept_states.append(next_state)

    def displayDFA(self, fileName='dfa.gv', projectName='deterministic_finite_state_machine'):
        outputDir = 'dfaOutput'
        os.makedirs(outputDir, exist_ok=True)
        dotFilePath = os.path.join(outputDir, fileName)
        graph = Digraph(projectName, filename=fileName, format='png')
        graph.attr(rankdir='LR')
        graph.attr('node', shape='doublecircle')
        for accept_state in self.dfa_accept_states:
            graph.node('s' + str(self.dfa_states[accept_state]))

        graph.attr('node', shape='circle')
        for from_state, transitions in self.dfa_transitions.items():
            for symbol, to_states in transitions.items():
                for to_state in to_states:
                    graph.edge('s' + str(self.dfa_states[from_state]), 's' + str(self.dfa_states[to_state]), label=symbol)

        graph.attr('node', shape='point')
        graph.edge('', 's' + str(self.dfa_states[self.dfa_start_state]))
        graph.render(filename=dotFilePath, directory=outputDir, view=False)