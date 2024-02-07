#Copyright (C), 2024-2025, bl33h
#FileName: shuntingYard.py
#Author: Sara Echeverria
#Version: I
#Creation: 02/02/2024
#Last modification: 06/02/2024

def shuntingYard():
    # loop to get a valid regular expression
    while True:
        infix = input("enter your regular expression: ")
        output = []
        operators = []
        errors = []
        # precedence of the operators with tokens
        precedence = {'*': 3, '+': 3, '|': 1, '.': 4, '?': 3}
        count = 0

        for token in infix:
            # error handling
            if token in '*+?|' and count == 0:
                errors.append(f"error: operation {token} without operands at the beginning.")
                break
            if token in '*+?' and (count + 1 == len(infix) or infix[count + 1] in '+*?|'):
                errors.append(f"error: operation {token} without operands.")
                break 
            if token.isalnum() or token in '[-]ε':
                output.append(token)
            elif token == '(':
                operators.append(token)
            elif token == ')':
                while operators and operators[-1] != '(':
                    output.append(operators.pop())
                if operators:
                    operators.pop()
                else:
                    errors.append("error: unbalanced parentheses. missing opening '('.")
                    break
            elif token in precedence:
                while operators and precedence.get(operators[-1], 0) >= precedence[token]:
                    output.append(operators.pop())
                operators.append(token)
            count += 1

        while operators:
            if operators[-1] == '(':
                errors.append("error: unbalanced parentheses. missing closing ')'.")
                break
            else:
                output.append(operators.pop())

        if not errors:
            return output
        else:
            for error in errors:
                print(error)
            print("please try again.")

result = shuntingYard()
if result:
    print("postfix notation:", ''.join(result))
