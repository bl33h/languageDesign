#Copyright (C), 2024-2025, bl33h 
#FileName: regexToAutomaton.py
#Author: Sara Echeverria 
#Version: I
#Creation: 11/02/2024
#Last modification: 07/02/2024
# References
# [Attaching NFA Fragments together (regexToAutomaton). (n.d.). Stack Overflow. https://stackoverflow.com/questions/50916898/attaching-nfa-fragments-together-regexToAutomaton]
# [automata-toolkit. (2021). PyPI. https://pypi.org/project/automata-toolkit/]
# [Martinez. (2023). Automata: An alternative NFA is generated by regexToAutomaton's Algorithm for Construction. CopyProgramming. https://copyprogramming.com/howto/regexToAutomaton-s-construction-algorithm-produces-a-different-nfa]

from oldSchoolDfa.shuntingYard import *

# ------- mcnaughton yamada thompson method to convert regex to nfa -------     
class thompson:
    def __init__(self, regex):
        self.regex = regex
        self.createNFA()

    def comparePrecedence(op):
        if op == orOperator:
            return 1
        elif op == concatenationOperator:
            return 2
        elif op == kleeneStar:
            return 3
        elif op == optionalOperator:
            return 3
        elif op == plusOperator:
            return 3
        else:       
            return 0

    def handleSymbol(inputSymbol):   
        initialState = 1
        nextState = 2
        basicregexToAutomaton = regexToAutomaton(set([inputSymbol]))
        basicregexToAutomaton.initialize(initialState)
        basicregexToAutomaton.acceptState(nextState)
        basicregexToAutomaton.createTransition(initialState, nextState, inputSymbol)
        return basicregexToAutomaton
    

    def handleOpt(a):
        [a, m1] = a.updateStates(2)  # Update states to accommodate for new transitions and states
        initialState = 1
        nextState = m1
        optionalRegexToAutomaton = regexToAutomaton(a.symbols)
        optionalRegexToAutomaton.initialize(initialState)
        optionalRegexToAutomaton.acceptState(nextState)
        optionalRegexToAutomaton.createTransition(optionalRegexToAutomaton.initialState, a.initialState, epsilon)
        optionalRegexToAutomaton.createTransition(optionalRegexToAutomaton.initialState, optionalRegexToAutomaton.acceptStates[0], epsilon)
        optionalRegexToAutomaton.createTransition(a.acceptStates[0], optionalRegexToAutomaton.acceptStates[0], epsilon)
        optionalRegexToAutomaton.saveTransitions(a.transitions)
        
        return optionalRegexToAutomaton

        
    def handlePlus(a):
        [a, m1] = a.updateStates(2)
        initialState = 1
        nextState = m1
        plusAutomaton = regexToAutomaton(a.symbols)
        plusAutomaton.initialize(initialState)
        plusAutomaton.acceptState(nextState)
        plusAutomaton.createTransition(initialState, a.initialState, epsilon)
        
        for acceptState in a.acceptStates:
            plusAutomaton.createTransition(acceptState, a.initialState, epsilon)
            plusAutomaton.createTransition(acceptState, nextState, epsilon)

        plusAutomaton.saveTransitions(a.transitions)
        return plusAutomaton


    def handlerOr(a, b):   
        [a, m1] = a.updateStates(2)
        [b, m2] = b.updateStates(m1)
        initialState = 1
        nextState = m2
        unionregexToAutomaton = regexToAutomaton(a.symbols.union(b.symbols))
        unionregexToAutomaton.initialize(initialState)
        unionregexToAutomaton.acceptState(nextState)
        unionregexToAutomaton.createTransition(unionregexToAutomaton.initialState, a.initialState, epsilon)
        unionregexToAutomaton.createTransition(unionregexToAutomaton.initialState, b.initialState, epsilon)
        unionregexToAutomaton.createTransition(a.acceptStates[0], unionregexToAutomaton.acceptStates[0], epsilon)
        unionregexToAutomaton.createTransition(b.acceptStates[0], unionregexToAutomaton.acceptStates[0], epsilon)
        unionregexToAutomaton.saveTransitions(a.transitions)
        unionregexToAutomaton.saveTransitions(b.transitions)
        return unionregexToAutomaton

    def handleConcatenation(a, b):    
        [a, m1] = a.updateStates(1)
        [b, m2] = b.updateStates(m1)
        initialState = 1
        nextState = m2 - 1
        concatenationregexToAutomaton = regexToAutomaton(a.symbols.union(b.symbols))
        concatenationregexToAutomaton.initialize(initialState)
        concatenationregexToAutomaton.acceptState(nextState)
        concatenationregexToAutomaton.createTransition(a.acceptStates[0], b.initialState, epsilon)
        concatenationregexToAutomaton.saveTransitions(a.transitions)
        concatenationregexToAutomaton.saveTransitions(b.transitions)
        return concatenationregexToAutomaton

    def handleKleeneStar(a):  
        [a, m1] = a.updateStates(2)
        initialState = 1
        nextState = m1
        kleeneregexToAutomaton = regexToAutomaton(a.symbols)
        kleeneregexToAutomaton.initialize(initialState)
        kleeneregexToAutomaton.acceptState(nextState)
        kleeneregexToAutomaton.createTransition(kleeneregexToAutomaton.initialState, a.initialState, epsilon)
        kleeneregexToAutomaton.createTransition(kleeneregexToAutomaton.initialState, kleeneregexToAutomaton.acceptStates[0], epsilon)
        kleeneregexToAutomaton.createTransition(a.acceptStates[0], kleeneregexToAutomaton.acceptStates[0], epsilon)
        kleeneregexToAutomaton.createTransition(a.acceptStates[0], a.initialState, epsilon)
        kleeneregexToAutomaton.saveTransitions(a.transitions)
        return kleeneregexToAutomaton

    def createNFA(self):
        temp = ''
        prev = ''
        symbols = set()
        # process the regex
        for ch in self.regex:
            if ch in alphabet:
                symbols.add(ch)
            if ch in alphabet or ch == openParentheses:
                if prev != concatenationOperator and (prev in alphabet or prev in [kleeneStar, closedParentheses]): 
                    temp += concatenationOperator
            temp += ch
            prev = ch
        self.regex = temp
        temp = ''
        stack = []
        for ch in self.regex:
            if ch in alphabet:
                temp += ch 
            elif ch == openParentheses:
                stack.append(ch) 
            elif ch == closedParentheses:
                while stack[-1] != openParentheses:
                    temp += stack.pop()
                stack.pop()    
            else:
                while stack and thompson.comparePrecedence(stack[-1]) >= thompson.comparePrecedence(ch):
                    temp += stack.pop()
                stack.append(ch) 
        while stack:
            temp += stack.pop() 
        self.regex = temp

        # build NFA
        self.regexToAutomatonStack = []
        for ch in self.regex:
            if ch in alphabet:
                self.regexToAutomatonStack.append(thompson.handleSymbol(ch)) 
            elif ch == orOperator:
                b = self.regexToAutomatonStack.pop()
                a = self.regexToAutomatonStack.pop()
                self.regexToAutomatonStack.append(thompson.handlerOr(a, b)) 
            elif ch == concatenationOperator:
                b = self.regexToAutomatonStack.pop()
                a = self.regexToAutomatonStack.pop()
                self.regexToAutomatonStack.append(thompson.handleConcatenation(a, b))
            elif ch == kleeneStar:
                a = self.regexToAutomatonStack.pop()
                self.regexToAutomatonStack.append(thompson.handleKleeneStar(a))
            elif ch == optionalOperator:
                a = self.regexToAutomatonStack.pop()
                self.regexToAutomatonStack.append(thompson.handleOpt(a))
            elif ch == plusOperator:
                a = self.regexToAutomatonStack.pop()
                self.regexToAutomatonStack.append(thompson.handlePlus(a))
        self.nfa = self.regexToAutomatonStack.pop()
        self.nfa.symbols = symbols

    def analyzeNFA(self, string):
        print('\n------------\nNFA simulation')
        string = string.replace('@', epsilon)
        currentState = self.nfa.initialState
        currentState = self.nfa.epsilonManagement(currentState)

        for ch in string:
            if ch == epsilon:
                continue
            states = self.nfa.otherTransitions(currentState, ch)
            print(f"closure states: {states}, input symbol: {ch}, next state: {states}")
            currentState = set()
            for s in states:
                currentState = currentState.union(self.nfa.epsilonManagement(s))
            print(f"closure states: {currentState}, input symbol: {epsilon}, next state: {currentState}")
        if currentState.intersection(self.nfa.acceptStates):
            print(f"\nstring '{string}' accepted.")
        else:
            print(f"\nstring '{string}' not accepted, stops at state {currentState}.")
        return currentState.intersection(self.nfa.acceptStates)

    def displayNFA(self):
        self.nfa.display('nfa.gv', 'nondeterministicFiniteStateMachine')