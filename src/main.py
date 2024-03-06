# Copyright (C), 2024-2025, bl33h 
# FileName: main.py
# Author: Sara Echeverria
# Version: I
# Creation: 06/02/2024
# Last modification: 11/02/2024

from directDfa.directDfaBuilder import directMethodDfa
from directDfa.regexUtilities import errorManagement
from lexicalAnalyzer.reader import yalexParser
from oldSchoolDfa.thompson import thompson
from oldSchoolDfa.subsets import *

def mainMenu():
    print("\n------- welcome to your finite automaton kit generator -------")
    print("- for regex to NFA and DFA with its minimization insert [1.]")
    print("- for regex to NFA by direct method insert [2.]")
    print("- for a lexical analyzer insert [3.]")
    print("- to exit insert [4.]")
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
            file_path = 'src/yalexFiles/low.yal'
            char_sets, rules = yalexParser(file_path)
            print("character sets:", char_sets)
            print("\nrules:", rules)
        
        elif choice == '4':
            break

        else:
            print("invalid option. please try again.")

        # ask if the user wants to do another task after each action, except for exiting
        keepG = input("do you want to do another task? (yes/no): ")
        if keepG.lower() != 'yes':
            break