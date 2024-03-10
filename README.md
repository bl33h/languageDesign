# languageDesign - lexical analyzer
It's an advanced toolkit that integrates lexical analysis, parsing of regular expressions, syntax tree generation, direct DFA construction, and automata visualization. Leveraging powerful algorithms and a user-friendly interface

<p align="center">
  <br>
  <img src="https://miro.medium.com/v2/resize:fit:1400/0*vNg6gYCh-OMFlxAW.gif" alt="pic" width="500">
  <br>
</p>
<p align="center">
  <a href="#Files">Files</a> •
  <a href="#Features">Features</a> •
  <a href="#how-to-use">How To Use</a> •
  <a href="#yal-files">YAL Files</a>
</p>

## Files
- **parser.py**: Main file that integrates all components, providing the core functionality of the toolkit.
- **ui.py**: Offers a graphical user interface for interacting with the toolkit, including file management and lexical analysis.
- **config.py**: Contains configurations and definitions used across the toolkit.
- **directDfaBuilder.py**: Implements the direct DFA construction algorithm from regular expressions.
- **parserUtilities.py, regexUtilities.py**: Provide utility functions for parsing and managing regular expressions.
- **syntaxTree.py**: Contains logic for generating and managing syntax trees from regular expressions.
- **high.yal, low.yal, medium.yal**: Define lexical rules and structures using a custom syntax, crucial for specifying the lexical elements for analysis.

## Features
The main features of the application include:

- Lexical Analysis: Parses and tokenizes input files, including .yal files, to prepare for further processing.
- Regular Expression Parsing: Converts regular expressions into a more manageable form for processing.
- Syntax Tree Generation: Constructs syntax trees from parsed regular expressions, facilitating the understanding of their structure.
- Direct DFA Construction: Builds deterministic finite automata directly from regular expressions, bypassing the need for NFA construction.
- Automata Visualization: Utilizes Graphviz to create visual representations of finite automata, enhancing comprehension and analysis.
- User-Friendly Interface: Offers a graphical interface for easier interaction with the toolkit, including file operations and analysis execution.
- YAL File Processing: Analyzes .yal files to extract and process lexical rules and structures.

## YAL Files
.yal files are an integral part of the project, allowing users to define lexical rules and structures in a custom syntax. These files are used to specify the lexical elements that the parser will analyze, providing a flexible and powerful way to customize the lexical analysis process. Examples include high.yal, low.yal, and medium.yal, each defining different levels of complexity in lexical rules.

## How To Use
To clone and run this application, you'll need [Git](https://git-scm.com), [Python](https://www.python.org/downloads/) and  [Graphviz](https://graphviz.org) installed on your computer. From your command line:

```bash
# Clone this repository
$ git clone https://github.com/bl33h/languageDesign/

# Branch switch
$ git checkout lexicalAnalyzer

# Run the program
$ cd src
$ python main.py
```