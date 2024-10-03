# Copyright (C), 2024-2025, bl33h
# File: A tokenizer for the yaleX file
# Author: Sara Echeverria

import pickle

# tokens list
tokens = []

# returns
word = 'word'
WORD = 'WORD'
NUMBER = 7
WHITESPACE = ' '
PLUS = '+'
TIMES = '*'
DOT = '.'
MINUS = '-'
ID = 'ID'
PERCENTAGE = '%'
CHARACTER = '_'
DOLLAR = '$'
DIVIDE = '/'
TOKEN = '%' + 'token'
TWOPOINTS = ':'
FINISHDECLARATION = ';'
LPAREN = '('
RPAREN = ')'
EQUALS = '='
AND = '&'
GREATERCHAR = '<'

# pickle use
with open('miedumYalYalpTokens', 'rb') as f:
	tokens = pickle.load(f)

def tokenReturns(symbol):
	if symbol == 'delim':
		None
	if symbol == 'ws':
		return WHITESPACE
	if symbol == 'letter':
		None
	if symbol == 'digit':
		None
	if symbol == 'id':
		return ID
	if symbol == '+':
		return PLUS
	if symbol == '*':
		return TIMES
	if symbol == '(':
		return LPAREN
	if symbol == ')':
		return RPAREN

	return symbol

# iterating loop
for token in tokens:
	if(token[1] == '!Error'):
		print(f'→ Lexeme: {token[0]} | !No token found')
	else:
		temp = ''
		if '\n' in token[0] or token[0] == ' ' or token[0] == '':
			temp = repr(token[0])
		else:
			temp = token[0]
		print(f'→ Lexeme: {temp} | >Token: {tokenReturns(token[1])}')