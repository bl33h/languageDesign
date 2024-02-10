# Copyright (C), 2024-2025, bl33h
# FileName: main.py
# Author: Sara Echeverria
# Version: I
# Creation: 06/02/2024
# Last modification: 09/02/2024

from shuntingYard import shuntingYard
from thompson import thompson
from subsets import *

def mainMenu():
    print(" ------- welcome to your finite automaton kit generator ------- ")
    print("- for regex to NFA and DFA with its minimization insert [1.]")
    print("- for regex to NFA by direct method insert [2.]")
    print("- to exit insert [3.]")
    choice = input("\n option selected: ")
    return choice

if __name__ == "__main__":
    while True:
        choice = mainMenu()

        # regex to NFA and DFA with its minimization
        if choice == '1':
            while True:
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

            nfaCall = thompson(postfix)
            nfa = nfaCall.nfa
            nfa.display('nfaGraph', 'NFA Visualization')
            wString = input("Enter the string w: ")
            if nfaCall.analyzeNFA(wString):
                print(f"the string '{wString}' w∈L(r)")
            else:
                print(f"the string '{wString}' w∉L(r)")

            dfaCall = dfaFromNfa(nfa)
            dfaCall.displayDFA('dfaGraph', 'DFA Visualization')
            if dfaCall.simulateDFA(wString):
                print(f"the string '{wString}' also w∈L(r) in DFA simulation.")
            else:
                print(f"the string '{wString}' also w∉L(r) in DFA simulation.")

            minDfaCall = dfaFromNfa(nfa)
            minDfaCall.minimize()
            minDfaCall.displayMinimizedDFA('minDfa', 'Minimized DFA Visualization')
            if dfaCall.simulateMinimizedDFA(wString):
                print(f"the string '{wString}' also w∈L(r) in min DFA simulation.")
            else:
                print(f"the string '{wString}' also w∉L(r) in min DFA simulation.")
            
            another_task = input("do you want to do another task? (yes/no): ")
            if another_task.lower() != 'yes':
                break
        
        # regex to NFA by direct method
        elif choice == '2':
            print("hello")
            another_task = input("do you want to do another task? (yes/no): ")
            if another_task.lower() != 'yes':
                break
        
        # exit
        elif choice == '3':
            break

        else:
            print("invalid option. please try again.")