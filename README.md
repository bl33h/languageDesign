# languageDesign - lexical tokens
This is a core module in the **languageDesign** project that generates Python code based on the lexical rules defined in `.yal` files. It serves as the first stage of the compilation pipeline, ensuring proper token identification and generation.

<p align="center">
  <br>
  <img src="https://cdn.analyticsvidhya.com/wp-content/uploads/2020/05/rnn.gif" alt="pic" width="500">
  <br>
</p>
<p align="center">
  <a href="#Files">Files</a> •
  <a href="#Features">Features</a> •
  <a href="#how-to-use">How To Use</a> •
  <a href="#yal-files">YAL Files</a>
</p>

## Files
- **main.py**: Main file that integrates all components, providing the core functionality of the tokenizer.
- **tokenizer.py**: Responsible for the generation of Python files based on the rules and patterns defined in `.yal` files.
- **tokenUtilities.py**: Offers utility functions for handling tokens and managing various aspects of lexical analysis.

## Features
- **Token Generation**: Reads `.yal` files containing user-defined lexical rules and generates a `.py` file to tokenize input data.
- **Pattern Matching**: Uses regular expressions and other patterns defined in `.yal` files to identify tokens.
- **Utility Functions**: Additional helper functions (from **tokenUtilities.py**) streamline the process of managing tokens and their properties.

## YALEX Files
YAL (Yet Another Lexical) files are used to define the rules and structures that the tokenizer will convert into a Python file for token generation. These files specify the tokens, patterns, and conditions that need to be recognized.

**Examples:**
- **high.yal**: Defines complex lexical rules.
- **medium.yal**: Contains moderate lexical rule complexity.
- **low.yal**: Features simpler rules for testing.

## How To Use
To clone and run this application, you'll need [Git](https://git-scm.com), [Python](https://www.python.org/downloads/), and [Graphviz](https://graphviz.org) installed on your computer. From your command line:

```bash
# Clone this repository
$ git clone https://github.com/bl33h/languageDesign/

# Branch switch
$ git checkout lexicalTokens

# Run the program
$ cd src
$ python main.py
