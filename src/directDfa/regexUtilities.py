# Copyright (C), 2024-2025, bl33h 
# FileName: regexUtilities.py
# Author: Sara Echeverria
# Version: I
# Creation: 06/02/2024
# Last modification: 29/02/2024

from string import *
from directDfa.config import *

# augmented expression [1.]
def augmentedRegex(rgx: str):
    def l(s):
        q=[symbols['(']]
        for i in s:
            q.append(ord(i))
            q.append(op['|'])
        q.pop()
        q.append(symbols[')'])
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
        elif i in opSymbols and i!='#': a.append(opSymbols[i])
        else: a.append(ord(i[-1]))
    return optionalOp(a)

def concatenationOp(rgx:list[int]):
    z=[rgx[0]]
    x,y=[op['*'],symbols[')'],op['|']],[symbols['('],op['|']]
    for i in range(1,len(rgx)):
        if not (rgx[i] in x or rgx[i-1] in y): z.append(op['·'])
        z.append(rgx[i])
    z+=[op['.'],symbols['#']]
    return z

def optionalOp(rgx:list[int]):
    b=[]
    for i in rgx:
        if i!=op['?'] and i!=op['+']: b.append(i)
        else:
            c,j=0,[]
            while b:
                j.append(b.pop())
                if j[-1]==symbols['(']: c+=1
                if j[-1]==symbols[')']: c-=1
                if c==0: break
            if not j or c!=0: raise Exception('Invalid')
            j.reverse()
            b.append(symbols['('])
            b.extend(j)
            if i==op['?']:
                b+=[op['|'],symbols['ε']]
            else: # +
                b.extend(j); b.append(op['*'])
            b.append(symbols[')'])
    return b

def manageExpression(rgx:list[int])->list[int]:
    opr,out=[],[]; z={op['*'],op['.'],op['|']}
    for c in rgx:
        if c in z:
            while opr and opr[-1]!=symbols['('] and opr[-1]>=c:
                out.append(opr.pop())
            opr.append(c)
        elif c==symbols['(']:
            opr.append(c)
        elif c==symbols[')']:
            while opr and opr[-1]!=symbols['(']:
                out.append(opr.pop())
            if not opr or opr.pop()!=symbols['(']: raise Exception('invalid')
        else:
            out.append(c)
    while opr:
        if opr[-1]==symbols['(']: raise Exception('invalid')
        out.append(opr.pop())
    return out

expressionString = lambda rgx: repr(''.join([chr(i) if i < 1e5 else r_opSymbols[i] for i in rgx]))

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