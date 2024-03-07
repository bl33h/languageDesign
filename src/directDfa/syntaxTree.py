# Copyright (C), 2024-2025, bl33h 
# FileName: syntaxTree.py
# Author: Sara Echeverria
# Version: I
# Creation: 06/02/2024
# Last modification: 07/03/2024

# ------- node class for syntax tree construction -------
class node():
    def __init__(self, symbol, leftChild=None, rightChild=None, number=None):
        self.rightChild = rightChild
        self.leftChild = leftChild
        self.followingPos = set()
        self.nullable = False
        self.firstpos = set()
        self.lastpos = set()
        self.symbol = symbol
        self.number = number
        self.elements = []
        
    # leaves labeled [3.]
    def labeledNode(self, node):
        firstP = [n.number for n in node.firstpos]
        lastP = [n.number for n in node.lastpos]
        followP = [n.number for n in node.followingPos]
        self.elements.append([node.symbol, firstP, lastP, followP, node.number])
            
        if node.leftChild is not None:
            self.labeledNode(node.leftChild)
        if node.rightChild is not None:
            self.labeledNode(node.rightChild)

        return self.elements
    
    # nullable function [4.], first position function [5.], last position function [6.]
    def getPositions(self):
        if not self.symbol.isOperator:
            if self.symbol.label == 'ε':
                self.nullable = True
            else:
                self.firstpos.add(self)
                self.lastpos.add(self)
                self.nullable = False
        else:
            if self.symbol.label in "*+?":
                self.leftChild.getPositions()
                self.firstpos.update(self.leftChild.firstpos)
                self.lastpos.update(self.leftChild.lastpos)
                
                if (self.symbol.label in '*?' or self.leftChild.nullable):
                    self.nullable = True
                else:
                    self.nullable = False
                  
            elif self.symbol.label == "|":
                self.leftChild.getPositions()
                self.rightChild.getPositions()
                self.nullable = self.leftChild.nullable or self.rightChild.nullable
                
                self.firstpos.update(self.rightChild.firstpos)
                self.firstpos.update(self.leftChild.firstpos)
                self.lastpos.update(self.rightChild.lastpos)
                self.lastpos.update(self.leftChild.lastpos)
                
            elif self.symbol.label == ".":
                self.leftChild.getPositions()
                self.rightChild.getPositions()
                
                self.nullable = self.leftChild.nullable and self.rightChild.nullable
                
                if self.leftChild.nullable:
                    self.firstpos.update(self.leftChild.firstpos)
                    self.firstpos.update(self.rightChild.firstpos)
                else: 
                    self.firstpos.update(self.leftChild.firstpos)
                    
                if self.rightChild.nullable:
                    self.lastpos.update(self.leftChild.lastpos)
                    self.lastpos.update(self.rightChild.lastpos)
                else:
                    self.lastpos.update(self.rightChild.lastpos)
                
        self.followingPosition()

    # following position function [7.]
    def followingPosition(self):
        if self.symbol.isOperator:
            if self.symbol.label == ".":
                for position in self.leftChild.lastpos:
                    position.followingPos.update(self.rightChild.firstpos)
                
            elif self.symbol.label == "*" or self.symbol.label == "+":
                for position in self.leftChild.lastpos:
                    position.followingPos.update(self.leftChild.firstpos)
        
        elif self.symbol.label == "ε":
            pass

# syntax tree construction from regex [2.]
class syntaxTree():
    def __init__(self, postfixRegex):
        self.postfixRegex = postfixRegex
        self.root = None
        
    # leaves labeled [3.] pt2
    def generateTree(self):
        manageExpressionNodes = []
        positionsQ = 1
        
        for symbol in self.postfixRegex:
            if (not symbol.isOperator):
                newNode = node(symbol, number=positionsQ)
                manageExpressionNodes.append(newNode)
                positionsQ += 1
                
            else:
                if (symbol.label in '*?+'):
                    leftNewNode = manageExpressionNodes.pop()
                    newNode = node(symbol, leftNewNode)
                    manageExpressionNodes.append(newNode)
                    
                else:
                    rightNewNode = manageExpressionNodes.pop()
                    leftNewNode = manageExpressionNodes.pop()
                    newNode = node(symbol, leftNewNode, rightNewNode)
                    manageExpressionNodes.append(newNode)
          
        self.root = manageExpressionNodes.pop()                  
        return self.root
            
    def nodeBuilder(self, node, dot):
        if node is not None:
            dot.node(str(id(node)), str(node.symbol))
            
            if node.leftChild is not None:
                dot.edge(str(id(node)), str(id(node.leftChild)))
                self.nodeBuilder(node.leftChild, dot)
                
            if node.rightChild is not None:
                dot.edge(str(id(node)), str(id(node.rightChild)))
                self.nodeBuilder(node.rightChild, dot)