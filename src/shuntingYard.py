#Copyright (C), 2024-2025, bl33h
#FileName: shuntingYard.py
#Author: Sara Echeverria
#Version: I
#Creation: 02/02/2024
#Last modification: 06/02/2024

def shuntingYard(infix):
    output = []
    operators = []
    errors = []
    precedence = {'*': 3, '+': 3, '|': 1, '.': 2, '?': 3}  # Ajuste de precedencia para '.' a 2

    for i, token in enumerate(infix):
        if token in '*+?' and (i == 0 or infix[i - 1] in '+*?|('):
            errors.append(f"error: operation {token} without operands.")
            break
        elif token.isalnum() or token in '[-]ε':
            output.append(token)
        elif token == '(':
            operators.append(token)
        elif token == ')':
            while operators and operators[-1] != '(':
                output.append(operators.pop())
            if operators: operators.pop()
            else: errors.append("error: unbalanced parentheses. missing opening '('.")
        elif token in precedence:
            while operators and precedence.get(operators[-1], 0) >= precedence[token]:
                output.append(operators.pop())
            operators.append(token)

    while operators:
        if operators[-1] == '(':
            errors.append("error: unbalanced parentheses. missing closing ')'.")
            break
        output.append(operators.pop())

    if not errors:
        return ''.join(output)
    else:
        for error in errors:
            print(error)
        print("please, try again.")