from tkinter import filedialog, scrolledtext, messagebox
from lexicalAnalyzer.reader import yalexParser
from lexicalAnalyzer.reader import *
from oldSchoolDfa.subsets import *
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

    def update_lineNumbers(self, code_editor):
        self.config(state='normal')
        self.delete('1.0', 'end')
        num_lines = int(code_editor.index('end-1c').split('.')[0])
        lineNumberString = "\n".join(str(i) for i in range(1, num_lines + 1))
        self.insert('1.0', lineNumberString)
        self.config(state='disabled')

class simpleUserInt(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('bl33hs IDE')
        self.geometry('800x600')
        self.currentOpenFile = None
        self.create_widgets()

    def create_widgets(self):
        # menu for file operations and running code
        barMenu = tk.Menu(self)
        self.config(menu=barMenu)

        fileMenu = tk.Menu(barMenu, tearoff=0)
        fileMenu.add_command(label="Open", command=self.open_file)
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
        self.code_editor = scrolledtext.ScrolledText(editorFrame, undo=True, wrap='none', bg='#ececfc', fg='#000000')
        self.code_editor.pack(expand=True, fill='both')
        self.code_editor.bind('<KeyRelease>', self.onCodeChanged)
        self.code_editor.bind('<KeyPress>', lambda e: self.lineNumbers.update_lineNumbers(self.code_editor))

        # terminal
        self.output_area = scrolledtext.ScrolledText(self, height=10, background='#454B70', foreground='white')
        self.output_area.pack(expand=False, fill='x', side='bottom')
        self.output_area.insert(tk.END, "Output:\n")
        self.output_area.config(state='disabled')

    def onCodeChanged(self, event=None):
        self.lineNumbers.update_lineNumbers(self.code_editor)

    def open_file(self):
        filePath = filedialog.askopenfilename()
        if not filePath:
            return
        # update the current file path
        self.currentOpenFile = filePath  
        with open(filePath, 'r') as file:
            self.code_editor.delete('1.0', tk.END)
            self.code_editor.insert('1.0', file.read())
        self.output_area.config(state='normal')
        self.output_area.delete('1.0', tk.END)
        self.output_area.insert(tk.END, "\nFile opened: " + self.currentOpenFile)
        self.output_area.config(state='disabled')

    def saveFile(self):
        if self.currentOpenFile is None:
            filePath = filedialog.asksaveasfilename(defaultextension="txt")
            if not filePath:
                return
            self.currentOpenFile = filePath
        with open(self.currentOpenFile, 'w') as file:
            code = self.code_editor.get('1.0', tk.END)
            file.write(code)
            messagebox.showinfo("Save", "File Saved Successfully")

    def analyzeLexically(self):
        if not self.currentOpenFile:
            messagebox.showwarning("Warning", "Please open and save a file first.")
            return
        
        # redirect stdout and stderr
        originalStdout = sys.stdout
        originalStderr = sys.stderr
        sys.stdout = textRedirector(self.output_area)
        sys.stderr = textRedirector(self.output_area)

        try:
            yalexInput = self.currentOpenFile
            char_sets, rules = yalexParser(yalexInput)
            print("character sets:", char_sets)
            print("\nrules:", rules)
            messagebox.showinfo("Analyze Lexically", "Analysis Completed Successfully")
        except Exception as e:
            print(f"\nan error occurred: {e}")
        finally:
            # restore original stdout and stderr
            sys.stdout = originalStdout
            sys.stderr = originalStderr