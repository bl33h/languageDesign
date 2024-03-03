# Copyright (C), 2024-2025, bl33h 
# FileName: config.py
# Author: Sara Echeverria
# Version: I
# Creation: 06/02/2024
# Last modification: 29/02/2024

# symbols and operators (epsilon, and operations: #, (, ), [, ], +, ?, ., |, *
symbols = {x: int(1e5) + i for i, x in enumerate('ε#()[]')}
op = {x: int(1.1e5) + i for i, x in enumerate('+?·|*')}
opSymbols = {**op, **symbols}