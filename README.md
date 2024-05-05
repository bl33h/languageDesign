# languageDesign - syntactic tokens
This toolkit integrates lexical and syntax analysis, parsing of regular expressions with token validation and LR(0) diagram generation based on YAPar and YALex files.

<p align="center">
  <br>
  <img src="https://cdn.dribbble.com/users/4358240/screenshots/14825308/media/84f51703b2bfc69f7e8bb066897e26e0.gif" alt="pic" width="500">
  <br>
</p>
<p align="center">
  <a href="#Files">Files</a> •
  <a href="#Features">Features</a> •
  <a href="#how-to-use">How To Use</a> •
  <a href="#yapar-yalp-files">YAPar & YALP Files</a>
</p>

## Files
- **yalpParser.py**: Responsible for parsing `.yalp` files containing user-defined lexical rules and structures.
- **directDfaBuilder.py**: Implements the direct DFA construction algorithm from regular expressions, it shows up the automaton and the LR0 diagram.
- **main.py**: Main file integrating all components, providing the core functionality of the toolkit.

## Features
- **Token Validation**: The **yalpParser** module parses `.yalp` files containing user-defined lexical rules and structures, verifies tokens against these rules, and provides feedback on validity. Features include:
  - Parsing `.yal` files to extract and process lexical rules into recognizable tokens.
  - Validating tokens by comparing them to the defined patterns.
  - Reporting errors when tokens don't match specified patterns.

- **LR(0) Diagram**: The LR(0) diagram provides a visual representation of the state transitions during parsing. Features include:
  - Automata Visualization: The **directDfaBuilder** module builds deterministic finite automata from regular expressions and uses Graphviz to represent them visually.
  - Syntax Analysis: Identifies valid or erroneous token sequences based on the predefined grammar.

## YAPAR & YALEX Files
Both YAPar and YALex files are crucial in defining the syntax and lexical structures that the parser uses to generate the LR(0) diagram and validate tokens.

- **YAPAR Files:** Define the grammar and syntax rules, used to generate the syntax analyzer and the LR(0) diagram.
- **YALEX Files:** Specify the lexical rules and structures that the analyzer will use to recognize tokens.

**Examples:**
- **highYalYalp.yalp**: Defines complex rules.
- **mediumYalYal.yalp**: Contains moderate rule complexity.
- **lowYalYal.yalp**: Features simpler rules for testing.

## How To Use
To clone and run this application, you'll need [Git](https://git-scm.com), [Python](https://www.python.org/downloads/), and [Graphviz](https://graphviz.org) installed on your computer. From your command line:

```bash
# Clone this repository
$ git clone https://github.com/bl33h/languageDesign/

# Branch switch
$ git checkout syntacticTokens

# Run the program
$ cd src
$ python main.py
