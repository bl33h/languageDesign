#Copyright (C), 2024-2025, bl33h
#FileName: subsets.py
#Author: Sara Echeverria
#Version: I
#Creation: 07/02/2024
#Last modification: 08/02/2024

from collections import defaultdict, deque
from thompson import Thompson
from thompson import NFA

class DFA:
    def __init__(self):
        self.states = []
        self.symbol_map = defaultdict(set)
        self.accept_states = set()
        self.initial_state = None
        self.transition_table = defaultdict(dict)

    def addState(self, state, is_accept=False):
        if state not in self.states:
            self.states.append(state)
            if is_accept:
                self.accept_states.add(state)

    def set_initial_state(self, state):
        self.initial_state = state

    def add_transition(self, from_state, to_state, symbol):
        self.symbol_map[symbol].add((from_state, to_state))
        self.transition_table[from_state][symbol] = to_state

def epsilonClosure(thompson, states):
    closure = set(states)
    stack = list(states)
    
    while stack:
        state = stack.pop()
        for to_state in thompson.epsilon_transitions(state):
            if to_state not in closure:
                closure.add(to_state)
                stack.append(to_state)
    
    return closure

def move(thompson, states, symbol):
    new_states = set()
    for state in states:
        new_states |= thompson.transition(state, symbol)
    return new_states

def NFAtoDFA(thompson):
    dfa = DFA()
    initial_closure = epsilonClosure(thompson, [thompson.initial_state])
    unmarked_states = deque([frozenset(initial_closure)])
    state_names = {frozenset(initial_closure): 0}
    dfa.set_initial_state(0)
    
    while unmarked_states:
        current_states = unmarked_states.popleft()
        for symbol in thompson.symbols - {thompson.epsilon}:
            move_closure = epsilonClosure(thompson, move(thompson, current_states, symbol))
            if not move_closure:
                continue
            move_closure_frozenset = frozenset(move_closure)
            if move_closure_frozenset not in state_names:
                state_names[move_closure_frozenset] = len(state_names)
                unmarked_states.append(move_closure_frozenset)
                if thompson.accept_states & move_closure:
                    dfa.addState(state_names[move_closure_frozenset], is_accept=True)
            dfa.add_transition(state_names[current_states], state_names[move_closure_frozenset], symbol)
    
    return dfa