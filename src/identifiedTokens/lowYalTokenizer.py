# Copyright (C), 2024-2025, bl33h
# File: A tokenizer for the yaleX file
# Author: Sara Echeverria
import pickle
tokens = []
with open('tokens/lowTokens', 'rb') as f:
	tokens = pickle.load(f)

	if symbol == '	':
		None
	if symbol == '	':
		None
	if symbol == '	':
		None
	if symbol == '	':
		None
	if symbol == '	':
		None
	if symbol == '	':
		None
	if symbol == '	':
		None
	if symbol == '	':
		None
	if symbol == '	':
		None
def tokens_returns(symbol):

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
		print(f'→ Lexeme: {temp} | >Token: {tokens_returns(token[1])}')


