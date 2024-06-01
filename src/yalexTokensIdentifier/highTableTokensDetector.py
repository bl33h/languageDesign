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
with open('highTableTokens', 'rb') as f:
	tokens = pickle.load(f)

def tokenReturns(symbol):
	if symbol == 'delim':
		None
	if symbol == 'capLetter':
		None
	if symbol == 'lowerCaseLetter':
		None
	if symbol == 'digit':
		None
	if symbol == 'lowerLetter':
		None
	if symbol == 'capitalLetter':
		None
	if symbol == 'number':
		return NUMBER
	if symbol == 'ws':
		None
	if symbol == 'id':
		return ID
	if symbol == '':
		None
	if symbol == '+':
		return PLUS
	if symbol == '*':
		return TIMES
	if symbol == '(':
		return LPAREN
	if symbol == ')':
		return RPAREN
	if symbol == '<':
		return GREATER
	if symbol == '>':
		return GREATER
	if symbol == '=':
		return EQUALS
	if symbol == ';':
		return SEMICOLON
	if symbol == 'if':
		return IF

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