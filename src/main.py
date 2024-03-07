# Copyright (C), 2024-2025, bl33h 
# FileName: main.py
# Author: Sara Echeverria
# Version: I
# Creation: 06/02/2024
# Last modification: 07/03/2024

from tkinter import *
import customtkinter as ct
from lexicalAnalyzer.ui import simpleUserInt

def main():
    win = ct.CTk(fg_color="#ececfc")
    ct.set_appearance_mode("light")
    win.title("bl33h's compiler")
    
    # Add the following line to set the window icon
    win.iconbitmap("src/assets/icon.ico")
    
    etiWelcome = ct.CTkLabel(win, text="Welcome to the bl33h's compiler builder", font=("Arial", 16, "bold"), text_color="#454B70")
    etiWelcome.pack(pady=7)
    
    etiWelcome2 = ct.CTkLabel(win, text="Below you will find the first two phases to build a compiler: Lexical and syntactic analyzer.", font=("Arial", 11, "normal"), text_color="#2D3041")
    etiWelcome3 = ct.CTkLabel(win, text="For both parts, the respective algorithms have been implemented correctly.", font=("Arial", 11, "normal"), text_color="#2D3041")
    etiWelcome2.pack(pady=0)
    etiWelcome3.pack(pady=0)

    buttonLexicalAnalyzer = ct.CTkButton(win, text="Lexical analyzer", fg_color="#797fa2", hover_color="#454B70", command=showLexicalAnalyzerUI)
    buttonLexicalAnalyzer.pack(pady=7)
    
    buttonSyntaxAnalyzer = ct.CTkButton(win, text="Syntax analyzer", fg_color="#797fa2", hover_color="#454B70", command=showSyntaxAnalyzerUI)
    buttonSyntaxAnalyzer.pack(pady=7)

    win.geometry("500x200")
    win.mainloop()

def showLexicalAnalyzerUI():
    app = simpleUserInt()
    app.mainloop()
    
def showSyntaxAnalyzerUI():
    pass

if __name__ == '__main__':
    main()