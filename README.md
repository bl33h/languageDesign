# languageDesign - finite automaton kit
It's a project that provides a comprehensive toolkit for generating and visualizing finite automata from regular expressions. It supports direct DFA generation, NFA to DFA conversion with minimization, and offers utilities for regex parsing and visualization using Graphviz.

<p align="center">
  <br>
  <img src="https://mechomotive.com/wp-content/uploads/2021/07/I1-11.gif" alt="pic" width="500">
  <br>
</p>

<p align="center">
  <a href="#Files">Files</a> •
  <a href="#Features">Features</a> •
  <a href="#how-to-use">How To Use</a>
</p>

## Files
- **main.py**: The entry point of the application, handling user input and coordinating the overall functionality.
- **shuntingYard.py**: Implements the Shunting Yard algorithm for parsing regular expressions into a format suitable for NFA generation.
- **thompson.py**: Contains the Thompson's construction algorithm for converting parsed regular expressions into NFAs.
- **subsets.py**: Provides the subset construction algorithm for converting NFAs into DFAs.
- **directDfa.py**: Implements the direct method for generating DFAs from regular expressions.

## Features
The main features of the application include:

- Regular Expression to NFA: Utilizes the Thompson's construction algorithm to convert regular expressions into Non-deterministic Finite Automata (NFA).
- NFA to DFA Conversion: Transforms NFAs into Deterministic Finite Automata (DFA) using the subset construction method.
- DFA Minimization: Implements DFA minimization to simplify the automaton without altering the language it recognizes.
- Direct DFA Generation: Directly constructs a DFA from a given regular expression using a direct method, bypassing the NFA stage.
- Regex Validation: Before processing, validates the input regular expressions for syntax errors such as unmatched parentheses or operations without operands.
- Visualization: Generates graphical representations of automata using Graphviz, aiding in the understanding and analysis of the automaton structure.
- Simulation: Simulates the operation of the DFA on input strings, determining whether the strings are accepted by the automaton.

## How To Use
To clone and run this application, you'll need [Git](https://git-scm.com), [Python](https://www.python.org/downloads/) and  [Graphviz](https://graphviz.org) installed on your computer. From your command line:

```bash
# Clone this repository
$ git clone https://github.com/bl33h/languageDesign/tree/finiteAutomataKit

# Branch switch
$ git checkout finiteAutomataKit

# Run the program
$ cd src
$ python main.py
```