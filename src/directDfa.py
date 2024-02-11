#Copyright (C), 2024-2025, bl33h 
#FileName: directDfa.py
#Author: Sara Echeverria
#Version: I
#Creation: 06/02/2024
#Last modification: 11/02/2024
# References
# [Urbina. (2022). DFA DIRECTO. Google Docs. https://docs.google.com/presentation/d/1XTelAJ3XDQ49NNDzGuTGTrVueULPrZIT/edit#slide=id.p15]

from string import *
from graphviz import Digraph
import os

# ------- dfa convertion using the direct method -------
# symbols and operators (epsilon, and operations: #, (, ), [, ], +, ?, ., |, *
smb = {x: int(1e5) + i for i, x in enumerate('ε#()[]')}
op = {x: int(1.1e5) + i for i, x in enumerate('+?.|*')}
opsmb = {**op, **smb}

# augmented expression [1.]
def augmentedRegex(rgx: str):
    def l(s):
        q=[smb['(']]
        for i in s:
            q.append(ord(i))
            q.append(op['|'])
        q.pop()
        q.append(smb[')'])
        return q
    repl={
        '\d':l(digits),
        '\s':l(whitespace),
        '\w':l(ascii_letters+digits+'_'),
        '.': l(printable.replace('\n',''))
    }
    z=iter(rgx)
    a=[]
    for i in z:
        if i=='\\': i+=next(z)
        if i in repl: a.extend(repl[i])
        elif i in opsmb and i!='#': a.append(opsmb[i])
        else: a.append(ord(i[-1]))
    return optionalOp(a)

def concatenationOp(rgx:list[int]):
    z=[rgx[0]]
    x,y=[op['*'],smb[')'],op['|']],[smb['('],op['|']]
    for i in range(1,len(rgx)):
        if not (rgx[i] in x or rgx[i-1] in y): z.append(op['.'])
        z.append(rgx[i])
    z+=[op['.'],smb['#']]
    return z

def optionalOp(rgx:list[int]):
    b=[]
    for i in rgx:
        if i!=op['?'] and i!=op['+']: b.append(i)
        else:
            c,j=0,[]
            while b:
                j.append(b.pop())
                if j[-1]==smb['(']: c+=1
                if j[-1]==smb[')']: c-=1
                if c==0: break
            if not j or c!=0: raise Exception('Invalid')
            j.reverse()
            b.append(smb['('])
            b.extend(j)
            if i==op['?']:
                b+=[op['|'],smb['ε']]
            else: # +
                b.extend(j); b.append(op['*'])
            b.append(smb[')'])
    return b

def manageExpression(rgx:list[int])->list[int]:
    opr,out=[],[]; z={op['*'],op['.'],op['|']}
    for c in rgx:
        if c in z:
            while opr and opr[-1]!=smb['('] and opr[-1]>=c:
                out.append(opr.pop())
            opr.append(c)
        elif c==smb['(']:
            opr.append(c)
        elif c==smb[')']:
            while opr and opr[-1]!=smb['(']:
                out.append(opr.pop())
            if not opr or opr.pop()!=smb['(']: raise Exception('invalid')
        else:
            out.append(c)
    while opr:
        if opr[-1]==smb['(']: raise Exception('invalid')
        out.append(opr.pop())
    return out

expressionString = lambda rgx: repr(''.join([chr(i) if i < 1e5 else r_opsmb[i] for i in rgx]))
        
class Node:
    count=0
    nodelist={}

    def __init__(self,v:int,l=None,r=None):
        self.v=v
        self.c1=l
        self.c2=r
        self._id=None
        self.nullable=None
        self.firstpos=set()
        self.lastpos=set()
        self.followpos=set()
        if v<1e5+2: 
            Node.count+=1
            self._id=Node.count
            Node.nodelist[self._id]=self

    def __str__(self):
        return f'v={self.v} ,\nl={self.c1.v if self.c1 else None} , r={self.c2.v if self.c2 else None}\nid={self._id}'\
            f'\nnullable: {self.nullable}'\
            f'\nfpos: {self.firstpos} , lpos: {self.lastpos}'\
            f'\nflwpos: {self.followpos}'

# syntax tree construction from regex [2.]
class syntaxTree:
    def __init__(self,postfixRegex):
        self.__z=reversed(postfixRegex)
        self.root=Node(next(self.__z))
        self.symbols=set(i for i in postfixRegex if i<1e5+2 and i!=smb['ε'])
        self.generate(self.root)

    def generate(self,rt:Node):
        if rt.v==op['*']:
            rt.c1=Node(next(self.__z))
            self.generate(rt.c1)
        # operator
        elif rt.v>1e5+1: 
            rt.c2=Node(next(self.__z))
            self.generate(rt.c2)
            rt.c1=Node(next(self.__z))
            self.generate(rt.c1)
        rt.nullable=nullableFunc(rt)
        rt.firstpos=firstPosition(rt)
        rt.lastpos=lastPosition(rt)
        followingPosition(rt)
        
# leaves labeled [3.] & nullable function [4.]
def nullableFunc(n:Node):
    if n is None:
        return False
    # leaf node
    if n.c1==n.c2==None: 
        # epsilon management
        if n.v==smb['ε']: 
            return True
        if n._id:
            return False
    # operators
    if n.v==op['|']:
        return nullableFunc(n.c1) or nullableFunc(n.c2)
    if n.v==op['.']:
        return nullableFunc(n.c1) and nullableFunc(n.c2)
    if n.v==op['*']:
        return True

# first position function [5.]
def firstPosition(n:Node):
    if n.c1==n.c2==None:
        # epsilon management
        if n.v==smb['ε']: 
            return set()
        if n._id:
            return {n._id}
    if n.v==op['|']:
        return n.c1.firstpos | n.c2.firstpos
    if n.v==op['.']:
        return n.c1.firstpos | (n.c2.firstpos if n.c1.nullable else set())
    if n.v==op['*']:
        return n.c1.firstpos

# last position function [6.]
def lastPosition(n:Node):
    if n.c1==n.c2==None:
        # epsilon management
        if n.v==smb['ε']: 
            return set()
        if n._id:
            return {n._id}
    if n.v==op['|']:
        return n.c1.lastpos | n.c2.lastpos
    if n.v==op['.']:
        return n.c2.lastpos | (n.c1.lastpos if n.c2.nullable else set())
    if n.v==op['*']:
        return n.c1.lastpos

# following position function [7.]
def followingPosition(n:Node):
    if n.v==op['.']:
        for i in n.c1.lastpos:
            Node.nodelist[i].followpos |= n.c2.firstpos
    if n.v==op['*']:
        for i in n.lastpos:
            Node.nodelist[i].followpos |= n.firstpos


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
            if any(Node.nodelist[i].v==smb['#'] for i in state):
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
        print('\n------------\nDFA simulation')
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

# error management
def errorManagement (regex):
    # operations without operands
    if regex.startswith('*') or regex.startswith('?') or regex.startswith('+')or regex.startswith('|') or regex.startswith('.'):
        return "error: operation without operands."

    # balanced parentheses
    openParentheses = 0
    for char in regex:
        if char == '(':
            openParentheses += 1
        elif char == ')':
            openParentheses -= 1
            if openParentheses < 0: 
                return "error: unmatched closing parentheses."
    
    if openParentheses > 0:
        return "error: unmatched opening parentheses."
    
    return "OK"

# main function
def directMethodDfa(regex):
    rgx=manageExpression(concatenationOp(augmentedRegex(regex)))
    tree=syntaxTree(rgx)
    return directDfaBuilder().synTreeInitialState(tree)