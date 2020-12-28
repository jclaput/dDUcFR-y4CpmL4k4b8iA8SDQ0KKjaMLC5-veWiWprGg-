from tkinter import *
from tkinter import font
from tkinter.ttk import Treeview
from lolcode_lexer import *
from lolcode_parser import *
from lolcode_interpreter import *

import sys

# Code snippet for redirecting python console logs to tkinter GUI taken from:
# https://stackoverflow.com/questions/53721337/how-to-get-python-console-logs-on-my-tkinter-window-instead-of-a-cmd-window-whil

class PrintLogger(): 
    def __init__(self, textbox):
        self.textbox = textbox

    def write(self, text):
        self.textbox.insert(END, text)

    def flush(self):
        pass

def execute():
    codeOutputTextBox.configure(state='normal')
    codeOutputTextBox.delete("1.0", END)
    
    pl = PrintLogger(codeOutputTextBox)
    sys.stdout = pl

    lexemeTable = lexer(codeInputTextBox.get("1.0", END))
    myParser = Parser(lexemeTable)
    myParser()
    
    myInterpreter = Interpreter(myParser)
    myInterpreter()

    codeOutputTextBox.configure(state='disabled')

    lexemeTableTreeview.delete(*lexemeTableTreeview.get_children())
    symbolTableTreeview.delete(*symbolTableTreeview.get_children())

    # Populate lexemeTableTreeview with the results
    for l in lexemeTable:
        if l.tag == "TT_DELIMITER" and l.value not in ("HAI", "KTHXBYE"):
            continue
        
        if l.tag == "TT_END_OF_FILE":
            continue

        lexemeTableTreeview.insert('', 'end', values=(l.value, lexemeDescription[l.tag]))
    
    # # Populate symbolTableTreeview with the results
    for k,v in myInterpreter.symbolTable.items():
        symbolTableTreeview.insert('', 'end', values=(k, v["varValue"]))


window = Tk()
window.geometry("1280x720")
window.resizable(0, 0)
window.title("CMSC 124 LOLCODE Interpreter")

topFrame = Frame(window)
topFrame.pack(side=TOP, fill=X)
bottomFrame = Frame(window)
bottomFrame.pack(side=BOTTOM, fill=X)

codeInputTextBoxTabSettings = font.Font(
    family='System', size=12, weight='bold').measure('     ')
codeInputTextBox = Text(topFrame, width=60, borderwidth=1,
                        relief="solid", tabs=codeInputTextBoxTabSettings, font=("System"))
codeInputTextBox.insert(END, 
    "HAI" + "\n" +
    "\tVISIBLE \"HELLO WORLD\"" + "\n"
    "KTHXBYE" + "\n"
)
codeInputTextBox.pack(side=LEFT)

lexemeTableCols = ('Lexeme', 'Classification')
lexemeTableTreeview = Treeview(
    topFrame, columns=lexemeTableCols, show='headings')
for col in lexemeTableCols:
    lexemeTableTreeview.heading(col, text=col)
lexemeTableTreeview.pack(side=LEFT, fill=Y)

symbolTableCols = ('Identifier', 'Value')
symbolTableTreeview = Treeview(
    topFrame, columns=symbolTableCols, show='headings')
for col in symbolTableCols:
    symbolTableTreeview.heading(col, text=col)
symbolTableTreeview.pack(side=LEFT, fill=Y)

# Need to set state to normal if you want to change the contents
executeButton = Button(bottomFrame, text="Execute", command=execute)
executeButton.pack(side=TOP, fill=X)
codeOutputTextBox = Text(bottomFrame, width=55,
                         state="disabled", font=("System"))
codeOutputTextBox.pack(side=BOTTOM, fill=X)


window.mainloop()
