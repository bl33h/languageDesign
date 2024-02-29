#Copyright (C), 2024-2025, bl33h 
#FileName: directDfa.py
#Author: Sara Echeverria
#Version: I
#Creation: 06/02/2024
#Last modification: 29/02/2024
# References
# [Urbina. (2022). DFA DIRECTO. Google Docs. https://docs.google.com/presentation/d/1XTelAJ3XDQ49NNDzGuTGTrVueULPrZIT/edit#slide=id.p15]

from directDfa.regexUtilities import *
from graphviz import Digraph
from directDfa.syntaxTree import *
from directDfa.regexUtilities import *
from string import *
import os

# ------- dfa convertion using the direct method -------
class directDfaBuilder:
    def __init__(self):
        self.__dtrans={} # transitions to use in table later
        self.startstate=None
        self.finalstates=set()
        self.trapstate=frozenset([-1])
    
    def displayDirectDFA(self, fileName='directDfaGraph', projectName='DirectMethodDFA'):
        outputDir = 'directDfaOutput'
        os.makedirs(outputDir, exist_ok=True)
        dotFilePath = os.path.join(outputDir, fileName)
        graph = Digraph(projectName, filename=dotFilePath, format='png')
        graph.attr(rankdir='LR')

        # initial node for the start state
        graph.node('start', shape='none', label='')
        graph.attr('node', shape='doublecircle')
        for finalState in self.finalstates:
            graph.node(finalState, label=finalState)

        graph.attr('node', shape='circle')
        # other states addition
        for state, transitions in self.__dtrans.items():
            if state not in self.finalstates:
                graph.node(state, label=state)

        # draw edge
        graph.edge('start', self.startstate)

        # draw the edges based on transitions
        for state, transitions in self.__dtrans.items():
            for symbol, nextState in transitions.items():
                graph.edge(state, nextState, label=symbol)

        graph.render(view=False)

    # stablish D as the initial state (roots first position) [8.]
    def synTreeInitialState(self,tree):
        dstates=[frozenset(tree.root.firstpos)]
        vis=set()
        statename={}
        while dstates:
            state=dstates.pop()
            if state in vis: continue
            vis.add(state)
            statename.setdefault(state,f's{len(statename)}')
            if any(Node.nodelist[i].v==symbols['#'] for i in state):
                self.finalstates.add(state)
            for a in tree.symbols:
                z=set()
                for i in state:
                    node=Node.nodelist[i]
                    if node.v==a:
                        z|=node.followpos
                if len(z):
                    z=frozenset(z)
                    dstates.append(z)
                    self.__dtrans.setdefault(state,{})
                    self[state][a]=z

        # accepting states stablishment with # [10.]
        self.startstate='s0'
        self.finalstates={statename[i] for i in self.finalstates}
        self.__dtrans={statename[k1]:{chr(k2):statename[self[k1][k2]] for k2 in self[k1]} for k1 in self.__dtrans}

        return self

    def move(self,current,symbol):
        if current==self.trapstate:
            return self.trapstate
        try:
            return self[current][symbol]
        except KeyError:
            return self.trapstate

    def simulate(self, txt):
        print('\n------------\ndirect DFA simulation')
        current = self.startstate
        print(f"closure: {current}")

        for c in txt:
            print(f"input symbol: {c}, current state: {current}")
            nextState = self.move(current, c)
            if nextState != self.trapstate:
                print(f"transition state: {nextState}")
                current = nextState
            else:
                print("no transition found. string rejected.")
                return False
        
        isAccepted = current in self.finalstates
        print(f"final state: {current}.")
        print(f"\nstring {'accepted' if isAccepted else 'rejected'}.")
        return isAccepted

    # transition table construction [9.]
    def transitionTable(self):
        from copy import deepcopy
        return deepcopy(self.__dtrans)

    def __getitem__(self,state):
        return self.__dtrans[state]

# main function
def directMethodDfa(regex):
    rgx=manageExpression(concatenationOp(augmentedRegex(regex)))
    tree=syntaxTree(rgx)
    return directDfaBuilder().synTreeInitialState(tree)