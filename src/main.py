#Copyright (C), 2024-2025, bl33h
#FileName: main.py
#Author: Sara Echeverria
#Version: I
#Creation: 06/02/2024
#Last modification: 08/02/2024

# main.py

from shuntingYard import shuntingYard
from thompson import thompson
from subsets import dfaFromNfa

if __name__ == "__main__":
    while True:  
        # infinite loop to keep asking for input until it's valid
        regex_input = input("enter the regular expression: ")
        success, result = shuntingYard(regex_input)

        if success:
            postfix = result
            break
        else:
            print("--- errors encountered ---")
            for error in result:
                print(error)
            print("please, try again.")

    nfa_builder = thompson(postfix)
    nfa = nfa_builder.nfa
    
    nfa.display('nfaGraph', 'NFA Visualization')

    string_w = input("Enter the string w: ")
    if nfa_builder.analyzeNFA(string_w):
        print(f"the string '{string_w}' w∈L(r)")
    else:
        print(f"the string '{string_w}' w∉L(r)")

    dfa_builder = dfaFromNfa(nfa)
    dfa_builder.displayDFA('dfaGraph', 'DFA Visualization')
