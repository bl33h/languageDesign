#Copyright (C), 2024-2025, bl33h
#FileName: main.py
#Author: Sara Echeverria
#Version: I
#Creation: 06/02/2024
#Last modification: 08/02/2024

from shuntingYard import shuntingYard   
from thompson import thompson
from subsets import DFAFromNFA

if __name__ == "__main__":
    regex_input = input("enter the regular expression: ")
    postfix = shuntingYard(regex_input)
    nfa_builder = thompson(postfix)
    nfa = nfa_builder.nfa
    
    nfa.display('nfa_graph', 'NFA Visualization')

    string_w = input("enter the string w: ")
    if nfa_builder.analyzeNFA(string_w):
        print(f"the string'{string_w}' w∈L(r)")
    else:
        print(f"the string'{string_w}' w∉L(r)")

    dfaFromNfa = DFAFromNFA(nfa)
    dfaFromNfa.displayDFA('dfa_graph', 'DFA Visualization')