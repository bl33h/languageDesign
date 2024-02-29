# Copyright (C), 2024-2025, bl33h 
# FileName: syntaxTree.py
# Author: Sara Echeverria
# Version: I
# Creation: 06/02/2024
# Last modification: 29/02/2024

from string import *
from directDfa.config import *

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
        self.symbols=set(i for i in postfixRegex if i<1e5+2 and i!=symbols['ε'])
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
        if n.v==symbols['ε']: 
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
        if n.v==symbols['ε']: 
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
        if n.v==symbols['ε']: 
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