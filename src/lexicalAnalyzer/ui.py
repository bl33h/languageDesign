# Copyright (C), 2024-2025, bl33h 
# FileName: reader.py
# Author: Sara Echeverria
# Version: I
# Creation: 06/03/2024
# Last modification: 07/03/2024

from tkinter import filedialog, scrolledtext, messagebox
from directDfa.directDfaBuilder import *
from directDfa.regexUtilities import *
from lexicalAnalyzer.parser import *
from directDfa.syntaxTree import *
from directDfa.config import *
import tkinter as tk
import sys

class textRedirector(object):
    def __init__(self, widget):
        self.widget = widget

    def write(self, str):
        self.widget.config(state='normal')
        self.widget.insert('end', str)
        self.widget.see('end')
        self.widget.config(state='disabled')

    def flush(self):
        pass

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

class simpleUserInt(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("bl33h's Lexical Analyzer")
        self.geometry('1350x920')
        self.iconbitmap('src/assets/icon.ico')
        self.widgetsCreation()

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
        barMenu.add_cascade(label="Analyze", menu=analyzeMenu)

        # container for line numbers and code editor
        editorFrame = tk.Frame(self)
        editorFrame.pack(expand=True, fill='both')

        # line numbers
        self.lineNumbers = lineNumbersText(editorFrame, width=4)
        self.lineNumbers.pack(side='left', fill='y')

        # code editor
        self.codeEditor = scrolledtext.ScrolledText(editorFrame, undo=True, wrap='none', bg='#ececfc', fg='#000000')
        self.codeEditor.pack(expand=True, fill='both')
        self.codeEditor.bind('<KeyRelease>', self.onCodeChanged)
        self.codeEditor.bind('<KeyPress>', lambda e: self.lineNumbers.updateLineNumbers(self.codeEditor))

        # terminal
        self.outputA = scrolledtext.ScrolledText(self, height=10, background='#454B70', foreground='white')
        self.outputA.pack(expand=False, fill='x', side='bottom')
        self.outputA.config(state='disabled')

    def onCodeChanged(self, event=None):
        self.lineNumbers.updateLineNumbers(self.codeEditor)

    def openFile(self):
        filePath = filedialog.askopenfilename()
        if not filePath:
            return
        # update the current file path
        self.currentOpenFile = filePath  
        with open(filePath, 'r') as file:
            self.codeEditor.delete('1.0', tk.END)
            self.codeEditor.insert('1.0', file.read())
        self.outputA.config(state='normal')
        self.outputA.delete('1.0', tk.END)
        self.outputA.insert(tk.END, "\nFile opened: " + self.currentOpenFile)
        self.outputA.config(state='disabled')

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
            yal = yalexParser(self.currentOpenFile)
            unprocessedRegex, processedRegex, _= yal.read()
            
            # explicit shunting yard for the unprocessed and processed regex
            Obj = explicitShuntingYard(unprocessedRegex)
            Obj2 = explicitShuntingYard(processedRegex)
            
            # explicit postfix conversion for the unprocessed and processed regex (explicit concatenation)
            unpPostfixRegex = Obj.explicitPostfixConv()
            procPostfixRegex = Obj2.explicitPostfixConv()
            
            # get alphabet from the infix
            alphabet = Obj.getAlphabet()
            
            # place the augmented expression in a list
            augmentedExpression = augmentedRegex(unpPostfixRegex)

            # pr
            print()
            ls = [l.label if not l.isSpecialChar else repr(l.label) for l in augmentedExpression]
            print("=> postfix regex:\n", "".join(ls))
            print()

            print("-----  direct dfa from yal file  -----")
            print("features:")
            yalSynTree = directDfaBuilder(unprocessedRegex, procPostfixRegex, alphabet)
            yalexDirectDfa = yalSynTree.directDfaFromSynTree()
            print(yalexDirectDfa)
            print()
            displayDirectDfa(yalexDirectDfa)
            messagebox.showinfo("Analyze Lexically", "Analysis Completed Successfully")
            
        except Exception as e:
            print(f"\nan error occurred: {e}")
            
        finally:
            # restore original stdout and stderr
            sys.stdout = originalStdout
            sys.stderr = originalStderr