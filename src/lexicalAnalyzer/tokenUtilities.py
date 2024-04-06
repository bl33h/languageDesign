# Copyright (C), 2024-2025, bl33h 
# FileName: tokenUtilities.py
# Author: Sara Echeverria
# Version: I
# Creation: 05/04/2024
# Last modification: 06/04/2024

class tokenUtilities():
    def __init__(self, automatonInfo, w = None):
        self.automatonInfo = automatonInfo
        self.tokenList = []
        self.w = w
    
    # --- get the transitions of the automaton ---
    def moveTokens(self, states, symbol):
        newStates = []
        stack = []
        
        # check if the states is a list
        if (not isinstance(states, list)):
            stack.append(states)
        else:
            for i in states:
                stack.append(i)

        # get the new states
        while(len(stack)>0):
            t = stack.pop()
            for trans in self.automatonInfo.explicitTransitions:
                if(trans.inState == t and str(trans.symbol.label) == str(symbol)):
                    if(trans.fnState not in newStates):
                        newStates.append(trans.fnState)

        return newStates
    
    # --- simulate the dfa with the tokens ---
    def tokenSimulation(self, text):
        currentState = self.automatonInfo.initialState
        tokenMovements = []
        temp = ""
        
        # sequence work
        for i in range(len(text)):
            for j in range(len(text[i])):   
                temp += text[i][j]       
                currentState = self.moveTokens(currentState, text[i][j])
                
                # check if the current state is not empty
                if currentState:
                    if (j+1 < len(text[i])):
                        actualState = self.moveTokens(currentState, text[i][j+1])
                        
                        # check if the next state is empty
                        if not actualState:
                            newS = self.moveTokens(self.automatonInfo.initialState, temp)
                            
                            if newS:
                                if (newS == currentState):
                                    tokenMovements.append((temp, currentState))
                                else:
                                    tokenMovements.append((temp, newS))
                                    
                            else:
                                tokenMovements.append((temp, currentState))
                            currentState = self.automatonInfo.initialState
                            temp = ""
                            
                        else:
                            actualState = self.moveTokens(currentState, text[i][j+1])
                            if not actualState:
                                temp = ""
                         
                    else:
                        if (i+1 < len(text)):
                            for j in range(len(text[i+1])):
                                
                                if (j+1 < len(text[i+1])):
                                    actualState = self.moveTokens(currentState, text[i+1][j+1])
                                    
                                    if not actualState:
                                        tokenMovements.append((temp, currentState))
                                        currentState = self.automatonInfo.initialState
                                        temp = ""
                                        
                                    else:
                                        actualState = self.moveTokens(actualState, text[i][j+1])
                                        if not actualState:
                                            temp = ""
                                            
                                    break
                
                # errors management
                else:
                    currentState = self.automatonInfo.initialState
                    if (j+1 < len(text[i])):
                        actualState = self.moveTokens(currentState, text[i][j+1])
                        
                        # place the token error
                        if actualState:
                            tokenMovements.append((temp, "Error"))
                            temp = ""
                            actualState = self.moveTokens(actualState, text[i][j+1])
                            
                            if actualState:
                                currentState = self.automatonInfo.initialState
                    else:
                        tokenMovements.append((temp, "Error"))
                   
        return tokenMovements