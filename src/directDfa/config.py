# Copyright (C), 2024-2025, bl33h 
# FileName: config.py
# Author: Sara Echeverria
# Version: I
# Creation: 06/02/2024
# Last modification: 07/03/2024

from directDfa.regexUtilities import *

# ------- explicit shunting yard -------
class explicitShuntingYard(object):
    def __init__(self, expression):
        self.infix = expression
        self.precedence = {'*': 3, '+': 3, '?': 3,'.': 2, '|': 1, '(': 0, ')': 0, '': 0}
        self.operators = ['*', '.', '|', '+', '?']

    # manages the conversion from infix to postfix with explicit concatenation
    def explicitPostfixConv(self):
        infixRegex = []
        if(type(self.infix) == str):
            for i in self.infix:
                newSym = explicitSymbols(i)
                if i in self.operators or i in '()':
                    newSym.setType(True)
                infixRegex.append(newSym)
            self.infix = infixRegex
        
        expression = manageExpression()
        elementsQ = len(self.infix)
        currentInfixRegex = []
        postfixRegex = []
        
        # explicit concatenation
        for index in range(elementsQ):
            element = self.infix[index]
            currentInfixRegex.append(element) 
            if ((index+1) < len(self.infix)):
                if (element.isOperator):
                    if(element.label in '*+?)'):
                        if(not self.infix[index + 1].isOperator or self.infix[index + 1].label == '('):
                            dotSym = explicitSymbols('.')
                            dotSym.setType(True)
                            currentInfixRegex.append(dotSym) 
                elif (not element.isOperator):
                    if(not self.infix[index + 1].isOperator):
                        dotSym = explicitSymbols('.')
                        dotSym.setType(True)
                        currentInfixRegex.append(dotSym) 
                    elif(self.infix[index + 1].label == '('):
                        dotSym = explicitSymbols('.')
                        dotSym.setType(True)
                        currentInfixRegex.append(dotSym) 
                    elif(self.infix[index + 1].label == 'ε'):
                        dotSym = explicitSymbols('.')
                        dotSym.setType(True)
                        currentInfixRegex.append(dotSym) 
        
        # precedence placement
        for element in currentInfixRegex:
            if (element.isOperator and element.label == '('):
                expression.push(element)
                
            elif (element.isOperator and element.label == ')'):
                while (not expression.isEmpty() and expression.peek().label != '('):
                    postfixRegex.append(expression.pop())
                expression.pop()
            
            elif (element.isOperator and element.label in self.operators):
                while (not expression.isEmpty()):
                    el = expression.peek()
                    currentPrecedence = self.precedence[element.label]
                    lastPrecedence = self.precedence[el.label]

                    if (lastPrecedence >= currentPrecedence):
                        postfixRegex.append(expression.pop())
                        
                    else:
                        break
                    
                expression.push(element)    
                    
            else:
                postfixRegex.append(element)     
                    
        while (not expression.isEmpty()):
            postfixRegex.append(expression.pop())
                           
        return postfixRegex
    
    # ------- gets the alphabet from the infix expression -------
    def getAlphabet(self):
        alphabet = []
        for symbol in self.infix:
            if(not symbol.isOperator and symbol.label not in alphabet):
                alphabet.append(symbol.label)
                
        return sorted(alphabet)