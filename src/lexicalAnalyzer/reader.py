# Copyright (C), 2024-2025, bl33h 
# FileName: reader.py
# Author: Sara Echeverria
# Version: I
# Creation: 05/03/2024
# Last modification: 05/03/2024

def yalexParser(file_path):
    charSetsDict = {}
    rulesDict = {}
    currentSection = None
    
    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()
            if line.startswith('let'):
                parts = line.split('=')
                name_part = parts[0].strip()
                name = name_part.split()[1]
                chars = parts[1].strip().strip('[]')
                charSetsDict[name] = chars
            elif line.startswith('rule'):
                rule_name = line.split('=')[0].split()[1].strip()
                currentSection = rule_name
                rulesDict[currentSection] = ''
            elif currentSection and line:
                rulesDict[currentSection] += line + '\n'

    return charSetsDict, rulesDict