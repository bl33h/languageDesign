# Copyright (C), 2024-2025, bl33h
# File: A tokenizer for the yaleX file
# Author: Sara Echeverria

import pickle
tokens = []
word = 'word'
WORD = 'WORD'
NUMBER = 'NUMBER'
WHITESPACE = 'ws'
PLUS = '+'
TIMES = '*'
DOT = '.'
MINUS = '-'
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

with open('tokenizerTokens', 'rb') as f:
	tokens = pickle.load(f)

def tokenReturns(symbol):
	if symbol == 'lowerLetter':
		return word
	if symbol == 'capitalLetter':
		return WORD
	if symbol == 'number':
		return NUMBER
	if symbol == 'ws':
		return WHITESPACE
	if symbol == '+':
		return PLUS
	if symbol == '*':
		return TIMES
	if symbol == '.':
		return DOT
	if symbol == '-':
		return MINUS
	if symbol == '%':
		return PERCENTAGE
	if symbol == '_':
		return CHARACTER
	if symbol == '$':
		return DOLLAR
	if symbol == '/':
		return DIVIDE
	if symbol == '%token':
		return TOKEN
	if symbol == ':':
		return TWOPOINTS
	if symbol == ';':
		return FINISHDECLARATION
	if symbol == '(':
		return LPAREN
	if symbol == ')':
		return RPAREN
	if symbol == '=':
		return EQUALS
	if symbol == '&':
		return AND
	if symbol == '<':
		return GREATERCHAR

	return symbol

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