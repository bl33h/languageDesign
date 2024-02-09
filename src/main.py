#Copyright (C), 2024-2025, bl33h
#FileName: main.py
#Author: Sara Echeverria
#Version: I
#Creation: 06/02/2024
#Last modification: 09/02/2024

from shuntingYard import shuntingYard
from thompson import thompson
from subsets import *

if __name__ == "__main__":
    while True:  
        # infinite loop to keep asking for input until it's valid
        regex_input = input("enter the regular expression: ")
        success, result = shuntingYard(regex_input)

        if success:
            postfix = result
            break
        else:
            # error handling
            print("--- errors encountered ---")
            for error in result:
                print(error)
            print("please, try again.")

    # nfa
    nfaCall = thompson(postfix)
    nfa = nfaCall.nfa
    nfa.display('nfaGraph', 'NFA Visualization')
    string_w = input("enter the string w: ")
    if nfaCall.analyzeNFA(string_w):
        print(f"the string '{string_w}' w∈L(r)")
    else:
        print(f"the string '{string_w}' w∉L(r)")

    # dfa
    dfaCall = dfaFromNfa(nfa)
    dfaCall.displayDFA('dfaGraph', 'DFA Visualization')
    if dfaCall.simulateDFA(string_w):
        print(f"the string '{string_w}' also w∈L(r) in DFA simulation.")
    else:
        print(f"the string '{string_w}' also w∉L(r) in DFA simulation.")

    # min dfa
    minDfaCall = dfaFromNfa(nfa)
    minDfaCall.minimize()
    minDfaCall.displayMinimizedDFA('minDfa', 'Minimized DFA Visualization')