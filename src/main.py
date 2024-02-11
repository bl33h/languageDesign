# Copyright (C), 2024-2025, bl33h 
# FileName: main.py
# Author: Sara Echeverria
# Version: I
# Creation: 06/02/2024
# Last modification: 11/02/2024

from directDfa import directMethodDfa, errorManagement
from thompson import thompson
from subsets import *

def mainMenu():
    print("\n------- welcome to your finite automaton kit generator -------")
    print("- for regex to NFA and DFA with its minimization insert [1.]")
    print("- for regex to NFA by direct method insert [2.]")
    print("- to exit insert [3.]")
    choice = input("\nOption selected: ")
    return choice
    
if __name__ == "__main__":
    while True:
        choice = mainMenu()

        if choice == '1':
            regexInput = input('enter the regular expression: ')
            
            validationMessage = errorManagement(regexInput)

            while validationMessage != "OK":
                print(validationMessage)
                print("please re-enter the regular expression.")
                regexInput = input("enter the regular expression: ")
                validationMessage = errorManagement(regexInput)
                
            a = thompson(regexInput)
            a.displayNFA()
            
            wString = input("enter the string w: ")
            if a.analyzeNFA(wString):
                print(f"The string '{wString}' w∈L(r)")
            else:
                print(f"The string '{wString}' w∉L(r)")

            b = dfaFromNfa(a.nfa)
            b.displayDFA()
            if b.simulateDFA(wString):
                print(f"the string '{wString}' also w∈L(r) in DFA simulation.")
            else:
                print(f"the string '{wString}' also w∉L(r) in DFA simulation.")
            
            b.minimize()
            b.displayMinimizedDFA()
            if b.simulateMinimizedDFA(wString):
                print(f"the string '{wString}' also w∈L(r) in min DFA simulation.")
            else:
                print(f"the string '{wString}' also w∉L(r) in min DFA simulation.")
        
        elif choice == '2':
            regexInput = input("enter the regular expression: ")
            validationMessage = errorManagement(regexInput)

            while validationMessage != "OK":
                print(validationMessage)
                print("please re-enter the regular expression.")
                regexInput = input("enter the regular expression: ")
                validationMessage = errorManagement(regexInput)
                
            directDfaBuilder = directMethodDfa(regexInput)
            directDfaBuilder.displayDirectDFA(fileName='directDfaGraph', projectName='DirectMethodDFA')
            transitionTable = directDfaBuilder.transitionTable()
            wString = input("enter the string w: ")
            if directDfaBuilder.simulate(wString):
                print(f"the string '{wString}' w∈L(r)")
            else:
                print(f"the string '{wString}' w∉L(r)")
            
            print("\n------------\ntransitions table")
            for state, transitions in transitionTable.items():
                transitions_str = ', '.join([f"{symbol} -> {nextState}" for symbol, nextState in transitions.items()])
                print(f"State {state}: {transitions_str}")
        
        elif choice == '3':
            break

        else:
            print("invalid option. please try again.")

        # ask if the user wants to do another task after each action, except for exiting
        keepG = input("co you want to do another task? (yes/no): ")
        if keepG.lower() != 'yes':
            break