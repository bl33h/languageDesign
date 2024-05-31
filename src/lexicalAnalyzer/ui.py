# Copyright (C), 2024-2025, bl33h 
# FileName: reader.py
# Author: Sara Echeverria
# Version: I
# Creation: 06/03/2024
# Last modification: 05/04/2024

from tkinter import filedialog, scrolledtext, messagebox
from syntaxAnalyzer.syntaxGenerator import *
from directDfa.directDfaBuilder import *
from syntaxAnalyzer.yalpParser import *
from lexicalAnalyzer.tokenizer import *
from directDfa.regexUtilities import *
from lexicalAnalyzer.parser import *
from directDfa.syntaxTree import *
from tkinter import PanedWindow
from directDfa.config import *
import tkinter as tk
import pickle
import sys
import os

class textRedirector(object):
    def __init__(self, widget):
        self.widget = widget

    # write function
    def write(self, str):
        self.widget.config(state='normal')
        self.widget.insert('end', str)
        self.widget.see('end')
        self.widget.config(state='disabled')

# line numbers for the code editor
class lineNumbersText(tk.Text):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.config(state='disabled', bg='#797fa2', fg='#dbdcf3')

    def updateLineNumbers(self, codeEditor):
        self.config(state='normal')
        self.delete('1.0', 'end')
        num_lines = int(codeEditor.index('end-1c').split('.')[0])
        lineNumberString = "\n".join(str(i) for i in range(1, num_lines + 1))
        self.insert('1.0', lineNumberString)
        self.config(state='disabled')

# main class for the user interface
class simpleUserInt(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("bl33h's Lexical Analyzer")
        self.iconbitmap('src/assets/icon.ico')
        self.currentOpenFile = None
        self.geometry('1350x920')
        self.widgetsCreation()
        
    # widgets creation for the user interface
    def widgetsCreation(self):
        # menu for file operations and running code
        barMenu = tk.Menu(self)
        self.config(menu=barMenu)

        fileMenu = tk.Menu(barMenu, tearoff=0)
        fileMenu.add_command(label="Open", command=self.openFile)
        fileMenu.add_command(label="Save", command=self.saveFile)
        barMenu.add_cascade(label="File", menu=fileMenu)

        analyzeMenu = tk.Menu(barMenu, tearoff=0)
        analyzeMenu.add_command(label="Analyze Lexically", command=self.analyzeLexically)
        analyzeMenu.add_command(label="Identify Tokens", command=self.identifyTokens)
        barMenu.add_cascade(label="Options", menu=analyzeMenu)

        # main paned window
        mainPane = PanedWindow(self, orient='vertical', sashrelief='raised', sashwidth=5)
        mainPane.pack(fill='both', expand=True)

        # editor and line numbers pane
        editorFrame = tk.Frame(mainPane)
        mainPane.add(editorFrame, height=600)

        # line numbers
        self.lineNumbers = lineNumbersText(editorFrame, width=4)
        self.lineNumbers.pack(side='left', fill='y')

        # code editor
        self.codeEditor = scrolledtext.ScrolledText(editorFrame, undo=True, wrap='none', bg='#ececfc', fg='#000000')
        self.codeEditor.pack(expand=True, fill='both')
        self.codeEditor.bind('<KeyRelease>', self.onCodeChanged)
        self.codeEditor.bind('<KeyPress>', lambda e: self.lineNumbers.updateLineNumbers(self.codeEditor))
        self.lineNumbers.updateLineNumbers(self.codeEditor)

        # terminal pane
        terminalFrame = tk.Frame(mainPane)
        mainPane.add(terminalFrame, height=300)

        # clear terminal button
        clearTerminalButton = tk.Button(terminalFrame, text="Clear Terminal", command=self.clearTerminal)
        clearTerminalButton.pack(fill='x', side='top')

        self.outputA = scrolledtext.ScrolledText(terminalFrame, height=10, background='#454B70', foreground='white')
        self.outputA.pack(expand=True, fill='both')
        self.outputA.config(state='disabled')

    # clear terminal function
    def clearTerminal(self):
        self.outputA.config(state='normal')
        self.outputA.delete('1.0', tk.END)
        self.outputA.config(state='disabled')
    
    # code changed event
    def onCodeChanged(self, event=None):
        self.lineNumbers.updateLineNumbers(self.codeEditor)

    # open file function
    def openFile(self):
        filePath = filedialog.askopenfilename()
        if not filePath:
            return
        # update the current file path
        self.currentOpenFile = filePath  
        with open(filePath, 'r') as file:
            self.codeEditor.delete('1.0', tk.END)
            self.codeEditor.insert('1.0', file.read())
        # Update line numbers after loading file
        self.lineNumbers.updateLineNumbers(self.codeEditor)
        self.outputA.config(state='normal')
        self.outputA.delete('1.0', tk.END)
        self.outputA.insert(tk.END, "\nFile opened: " + self.currentOpenFile)
        self.outputA.config(state='disabled')

    # save file function
    def saveFile(self):
        if self.currentOpenFile is None:
            filePath = filedialog.asksaveasfilename(defaultextension="txt")
            if not filePath:
                return
            self.currentOpenFile = filePath
        with open(self.currentOpenFile, 'w') as file:
            code = self.codeEditor.get('1.0', tk.END)
            file.write(code)
            messagebox.showinfo("Save", "File Saved Successfully")

    # analyze lexically function (calls the parser)
    def analyzeLexically(self):
        if not self.currentOpenFile:
            messagebox.showwarning("Warning", "Please open and save a file first.")
            return
        
        # redirect stdout and stderr
        originalStdout = sys.stdout
        originalStderr = sys.stderr
        sys.stdout = textRedirector(self.outputA)
        sys.stderr = textRedirector(self.outputA)

        try:
            print("\n\nreading the yalex file...")
            yal = yalexParser(self.currentOpenFile)
            unprocessedRegex, processedRegex, yalDefs= yal.read()
            
            # explicit shunting yard for the unprocessed and processed regex
            Obj = explicitShuntingYard(unprocessedRegex)
            Obj2 = explicitShuntingYard(processedRegex)
            
            # explicit postfix conversion for the unprocessed and processed regex (explicit concatenation)
            unpPostfixRegex = Obj.explicitPostfixConv()
            procPostfixRegex = Obj2.explicitPostfixConv()
            
            # get alphabet from the infix
            alphabet = Obj2.getAlphabet()
            
            # place the augmented expression in a list
            augmentedExpression = augmentedRegex(unpPostfixRegex)

            ls = [l.label if not l.isSpecialChar else repr(l.label) for l in augmentedExpression]
            
            print("\n=> postfix regex:\n", "".join(ls))

            print("\n-----  direct dfa from yal file  -----")
            print("features:")
            yalSynTree = directDfaBuilder(processedRegex, procPostfixRegex, alphabet)
            yalexDirectDfa = yalSynTree.directDfaFromSynTree()
            print(yalexDirectDfa)
            displayDirectDfa(yalexDirectDfa)
            messagebox.showinfo("Analyze Lexically", "Analysis Completed Successfully")
        
        # error handling
        except Exception as e:
            print(f"\nan error occurred: {e}")
            
        finally:
            # restore original stdout and stderr
            sys.stdout = originalStdout
            sys.stderr = originalStderr
    
    def identifyTokens(self):
        if not self.currentOpenFile:
            messagebox.showwarning("Warning", "Please open and save a file first.")
            return
        
        # redirect stdout and stderr
        originalStdout = sys.stdout
        originalStderr = sys.stderr
        sys.stdout = textRedirector(self.outputA)
        sys.stderr = textRedirector(self.outputA)

        try:
            print("\n\nreading the yalex file...")
            yal = yalexParser(self.currentOpenFile)
            unprocessedRegex, processedRegex, yalDefs= yal.read()
            
            # explicit shunting yard for the unprocessed and processed regex
            Obj = explicitShuntingYard(unprocessedRegex)
            Obj2 = explicitShuntingYard(processedRegex)
            
            # explicit postfix conversion for the unprocessed and processed regex (explicit concatenation)
            unpPostfixRegex = Obj.explicitPostfixConv()
            procPostfixRegex = Obj2.explicitPostfixConv()
            
            # get alphabet from the infix
            unpAlphabet = Obj.getAlphabet()
            alphabet = Obj2.getAlphabet()
            
            # place the augmented expression in a list
            augmentedExpression = augmentedRegex(unpPostfixRegex)

            ls = [l.label if not l.isSpecialChar else repr(l.label) for l in augmentedExpression]
            
            print("\n=> postfix regex:\n", "".join(ls))

            print("\n-----  direct dfa from yal file  -----")
            print("features:")
            
            # unprocessed dfa
            unpYalSynTree = directDfaBuilder(unprocessedRegex, unpPostfixRegex, unpAlphabet)
            unpYalexDirectDfa = unpYalSynTree.directDfaFromSynTree()
            unpYalSynTree.unpAlphabet = unpAlphabet

            # processed dfa
            yalSynTree = directDfaBuilder(processedRegex, procPostfixRegex, alphabet)
            yalexDirectDfa = yalSynTree.directDfaFromSynTree()
            yalSynTree.alphabet = alphabet
            print(yalexDirectDfa)
            
            # show the success message
            messagebox.showinfo("Identify Tokens", "Tokens Identified Successfully")
            
            # remove the yal extension from the current file
            baseFileName = os.path.basename(self.currentOpenFile)
            noExtensionFile, _ = os.path.splitext(baseFileName)

            # construct the relative path to the tokenIdentifiers directory
            relativePath = os.path.join("..", "identifiedTokens")
            pickleDirectory = os.path.normpath(os.path.join(os.path.dirname(__file__), relativePath))
            picklePath = os.path.join(pickleDirectory, noExtensionFile)

            # create the directory if it doesn't exist
            if not os.path.exists(pickleDirectory):
                os.makedirs(pickleDirectory)

            # save the DFA to a pickle file
            with open(picklePath, 'wb') as f:
                pickle.dump(unpYalexDirectDfa, f)
                pickle.dump(yalexDirectDfa, f)
                pickle.dump(yalDefs, f)

            print("\n ✓Token identification and saving completed successfully.")
            
            name, _ = os.path.splitext(baseFileName)  
            tokenizerReader = tokenizer(f'src/identifiedTokens/{name}', 'src/yalexFiles/entry.txt')
            listToks = tokenizerReader.simulate()

            # show the tokens
            print("\n------- Identified tokens -------")
            tokensText = tokenizerReader.tokensList(listToks)

            # save the tokens
            tokenList = tokenizerReader.currentTokens(listToks)
            with open(f'src/tokens/{name}Tokens', 'wb') as f:
                pickle.dump(tokenList, f)

            # save the text tokens
            with open(f'src/tokens/{name}TextTokens', 'wb') as f:
                pickle.dump(tokensText, f)
                
            print()
            tokenizerReader.tokenizerBuilder(name)
            
            print("✓Tokenizer Python file generated successfully.")
                
        # error handling
        except Exception as e:
            print(f"\nan error occurred: {e}")
            
        finally:
            # restore original stdout and stderr
            sys.stdout = originalStdout
            sys.stderr = originalStderr

class syntaxAnalyzerUi(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("bl33h's Syntax Analyzer")
        self.iconbitmap('src/assets/icon.ico')
        self.currentOpenFile = None
        self.geometry('1350x920')
        self.widgetsCreation()
        
    # widgets creation for the user interface
    def widgetsCreation(self):
        # menu for file operations and running code
        barMenu = tk.Menu(self)
        self.config(menu=barMenu)

        fileMenu = tk.Menu(barMenu, tearoff=0)
        fileMenu.add_command(label="Open", command=self.openFile)
        fileMenu.add_command(label="Save", command=self.saveFile)
        barMenu.add_cascade(label="File", menu=fileMenu)

        analyzeMenu = tk.Menu(barMenu, tearoff=0)
        analyzeMenu.add_command(label="Identify Yal Tokens", command=self.identifyTokens)
        analyzeMenu.add_command(label="Validate Yal & Yalp Tokens", command=self.tokensValidator)
        analyzeMenu.add_command(label="Create SLR Table & Simulation", command=self.syntaxGenerator)
        barMenu.add_cascade(label="Options", menu=analyzeMenu)

        # main paned window
        mainPane = PanedWindow(self, orient='vertical', sashrelief='raised', sashwidth=5)
        mainPane.pack(fill='both', expand=True)

        # editor and line numbers pane
        editorFrame = tk.Frame(mainPane)
        mainPane.add(editorFrame, height=600)

        # line numbers
        self.lineNumbers = lineNumbersText(editorFrame, width=4)
        self.lineNumbers.pack(side='left', fill='y')

        # code editor
        self.codeEditor = scrolledtext.ScrolledText(editorFrame, undo=True, wrap='none', bg='#ececfc', fg='#000000')
        self.codeEditor.pack(expand=True, fill='both')
        self.codeEditor.bind('<KeyRelease>', self.onCodeChanged)
        self.codeEditor.bind('<KeyPress>', lambda e: self.lineNumbers.updateLineNumbers(self.codeEditor))
        self.lineNumbers.updateLineNumbers(self.codeEditor)

        # terminal pane
        terminalFrame = tk.Frame(mainPane)
        mainPane.add(terminalFrame, height=300)

        # clear terminal button
        clearTerminalButton = tk.Button(terminalFrame, text="Clear Terminal", command=self.clearTerminal)
        clearTerminalButton.pack(fill='x', side='top')

        self.outputA = scrolledtext.ScrolledText(terminalFrame, height=10, background='#454B70', foreground='white')
        self.outputA.pack(expand=True, fill='both')
        self.outputA.config(state='disabled')

    # clear terminal function
    def clearTerminal(self):
        self.outputA.config(state='normal')
        self.outputA.delete('1.0', tk.END)
        self.outputA.config(state='disabled')
    
    # code changed event
    def onCodeChanged(self, event=None):
        self.lineNumbers.updateLineNumbers(self.codeEditor)

    # open file function
    def openFile(self):
        filePath = filedialog.askopenfilename()
        if not filePath:
            return
        # update the current file path
        self.currentOpenFile = filePath  
        with open(filePath, 'r') as file:
            self.codeEditor.delete('1.0', tk.END)
            self.codeEditor.insert('1.0', file.read())
        # Update line numbers after loading file
        self.lineNumbers.updateLineNumbers(self.codeEditor)
        self.outputA.config(state='normal')
        self.outputA.delete('1.0', tk.END)
        self.outputA.insert(tk.END, "\nFile opened: " + self.currentOpenFile)
        self.outputA.config(state='disabled')

    # save file function
    def saveFile(self):
        if self.currentOpenFile is None:
            filePath = filedialog.asksaveasfilename(defaultextension="txt")
            if not filePath:
                return
            self.currentOpenFile = filePath
        with open(self.currentOpenFile, 'w') as file:
            code = self.codeEditor.get('1.0', tk.END)
            file.write(code)
            messagebox.showinfo("Save", "File Saved Successfully")
    
    # yal tokens identifier
    def identifyTokens(self):
        if not self.currentOpenFile:
            messagebox.showwarning("Warning", "Please open and save a file first.")
            return
        
        # redirect stdout and stderr
        originalStdout = sys.stdout
        originalStderr = sys.stderr
        sys.stdout = textRedirector(self.outputA)
        sys.stderr = textRedirector(self.outputA)

        try:
            print("\n\nreading the yalex file...")
            yal = yalexParser(self.currentOpenFile)
            unprocessedRegex, processedRegex, yalDefs= yal.read()
            
            # explicit shunting yard for the unprocessed and processed regex
            Obj = explicitShuntingYard(unprocessedRegex)
            Obj2 = explicitShuntingYard(processedRegex)
            
            # explicit postfix conversion for the unprocessed and processed regex (explicit concatenation)
            unpPostfixRegex = Obj.explicitPostfixConv()
            procPostfixRegex = Obj2.explicitPostfixConv()
            
            # get alphabet from the infix
            unpAlphabet = Obj.getAlphabet()
            alphabet = Obj2.getAlphabet()
            
            # place the augmented expression in a list
            augmentedExpression = augmentedRegex(unpPostfixRegex)

            ls = [l.label if not l.isSpecialChar else repr(l.label) for l in augmentedExpression]
            
            print("\n=> postfix regex:\n", "".join(ls))

            print("\n-----  direct dfa from yal file  -----")
            print("features:")
            
            # unprocessed dfa
            unpYalSynTree = directDfaBuilder(unprocessedRegex, unpPostfixRegex, unpAlphabet)
            unpYalexDirectDfa = unpYalSynTree.directDfaFromSynTree()
            unpYalSynTree.unpAlphabet = unpAlphabet

            # processed dfa
            yalSynTree = directDfaBuilder(processedRegex, procPostfixRegex, alphabet)
            yalexDirectDfa = yalSynTree.directDfaFromSynTree()
            yalSynTree.alphabet = alphabet
            print(yalexDirectDfa)
            
            # show the success message
            messagebox.showinfo("Identify Tokens", "Tokens Identified Successfully")
            
            # remove the yal extension from the current file
            baseFileName = os.path.basename(self.currentOpenFile)
            noExtensionFile, _ = os.path.splitext(baseFileName)

            # construct the relative path to the tokenIdentifiers directory
            relativePath = os.path.join("..", "identifiedTokens")
            pickleDirectory = os.path.normpath(os.path.join(os.path.dirname(__file__), relativePath))
            picklePath = os.path.join(pickleDirectory, noExtensionFile)

            # create the directory if it doesn't exist
            if not os.path.exists(pickleDirectory):
                os.makedirs(pickleDirectory)

            # save the DFA to a pickle file
            with open(picklePath, 'wb') as f:
                pickle.dump(unpYalexDirectDfa, f)
                pickle.dump(yalexDirectDfa, f)
                pickle.dump(yalDefs, f)

            print("\n ✓Token identification and saving completed successfully.")
            
            name, _ = os.path.splitext(baseFileName)  
            tokenizerReader = tokenizer(f'src/identifiedTokens/{name}', 'src/yalexFiles/entry.txt')
            listToks = tokenizerReader.simulate()

            # show the tokens
            print("\n------- Identified tokens -------")
            tokensText = tokenizerReader.tokensList(listToks)

            # save the tokens
            tokenList = tokenizerReader.currentTokens(listToks)
            with open(f'src/tokens/{name}Tokens', 'wb') as f:
                pickle.dump(tokenList, f)

            # save the text tokens
            with open(f'src/tokens/{name}TextTokens', 'wb') as f:
                pickle.dump(tokensText, f)
                
            print()
            tokenizerReader.tokenizerBuilder(name)
            
            print("✓Tokenizer Python file generated successfully.")
                
        # error handling
        except Exception as e:
            print(f"\nan error occurred: {e}")
            
        finally:
            # restore original stdout and stderr
            sys.stdout = originalStdout
            sys.stderr = originalStderr
    
    def tokensValidator(self):
        if not self.currentOpenFile:
            messagebox.showwarning("Warning", "Please open and save a file first.")
            return
        
        # redirect stdout and stderr
        originalStdout = sys.stdout
        originalStderr = sys.stderr
        sys.stdout = textRedirector(self.outputA)
        sys.stderr = textRedirector(self.outputA)

        try:
            print("\n\nvalidating the tokens...")
            # remove the yal extension from the current file
            baseFileName = os.path.basename(self.currentOpenFile)
            noExtensionFile, _ = os.path.splitext(baseFileName)
            parserInstance = yalpParser(f'src/yalpFiles/{noExtensionFile}.yalp', f'src/identifiedTokens/{noExtensionFile}', noExtensionFile)
            parserInstance.read()
            parserInstance.getGrammarSymbols()
            print("\n------ First Sets ------")
            for symbol in parserInstance.grammarSymbols:
                firstSet = parserInstance.first(symbol)
                print(f"First({symbol}): {firstSet}")

            print("\n------ Following Sets ------")
            for symbol in parserInstance.grammarSymbols:
                followingSet = parserInstance.following(symbol)
                print(f"Following({symbol}): {followingSet}")

            print("\n✓ LR0 automaton & diagram created successfully !\n")
        
        # error handling
        except Exception as e:
            print(f"\nan error occurred: {e}")
            
        finally:
            # restore original stdout and stderr
            sys.stdout = originalStdout
            sys.stderr = originalStderr
    
    def syntaxGenerator(self):
        if not self.currentOpenFile:
            messagebox.showwarning("Warning", "Please open and save a file first.")
            return
        
        # redirect stdout and stderr
        originalStdout = sys.stdout
        originalStderr = sys.stderr
        sys.stdout = textRedirector(self.outputA)
        sys.stderr = textRedirector(self.outputA)

        try:
            print("\n\ncreating SLR table & simulation...")
            # remove the yal extension from the current file
            baseFileName = os.path.basename(self.currentOpenFile)
            noExtensionFile, _ = os.path.splitext(baseFileName)
            parserInstance = syntaxGenerator(f'src/yalpFiles/{noExtensionFile}.yalp', f'src/identifiedTokens/{noExtensionFile}', f'src/tokens/{noExtensionFile}TextTokens', noExtensionFile)
            result = parserInstance.read()
            parserInstance.getGrammarSymbols()
            
            print()
            if type(result) == tuple:
                print(f"→ The file is ✘rejected (not accepted)\nConflict with {result[0]} for the following actions {','.join(result[1])}")
            else:
                print("→ The file is", result)
            print()
        
        # error handling
        except Exception as e:
            print(f"\nan error occurred: {e}")
            
        finally:
            # restore original stdout and stderr
            sys.stdout = originalStdout
            sys.stderr = originalStderr