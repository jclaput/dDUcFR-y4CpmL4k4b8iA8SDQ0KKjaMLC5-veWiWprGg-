from tkinter import *
from tkinter import font
from tkinter.ttk import Treeview
# from lexer import *
#
# def execute():
#     # Delete existing items in the lexemeTableTreeview
#     lexemeTableTreeview.delete(*lexemeTableTreeview.get_children())
#
#     # lexer analysis
#     lexemeTable = lexer(codeInputTextBox.get("1.0",END))
#
#     # Populate lexemeTableTreeview with the results
#     for l in lexemeTable:
#         lexemeTableTreeview.insert('', 'end', values=(l.value, lexemeDescription[l.classification]))


window = Tk()
window.geometry("1280x720")
window.resizable(0,0)
window.title("CMSC 124 LOLCODE Interpreter")

topFrame = Frame(window)
topFrame.pack(side=TOP, fill=X)
bottomFrame = Frame(window)
bottomFrame.pack(side=BOTTOM, fill=X)

codeInputTextBoxTabSettings = font.Font(family='System', size=12, weight='bold').measure('     ')
codeInputTextBox = Text(topFrame, width=60, borderwidth=1, relief="solid", tabs=codeInputTextBoxTabSettings, font=("System"))
codeInputTextBox.insert(END, "Hello World")
codeInputTextBox.pack(side=LEFT)

lexemeTableCols = ('Lexeme', 'Classification')
lexemeTableTreeview = Treeview(topFrame, columns=lexemeTableCols, show='headings')
for col in lexemeTableCols:
    lexemeTableTreeview.heading(col, text=col)
lexemeTableTreeview.pack(side=LEFT, fill=Y)


symbolTableCols = ('Identifier', 'Value')
symbolTableTreeview = Treeview(topFrame, columns=symbolTableCols, show='headings')
for col in symbolTableCols:
    symbolTableTreeview.heading(col, text=col)
symbolTableTreeview.pack(side=LEFT, fill=Y)

# Need to set state to normal if you want to change the contents
executeButton = Button(bottomFrame, text="Execute", command=execute)
executeButton.pack(side=TOP, fill=X)
codeOutputTextBox = Text(bottomFrame, width=55, state="disabled",font=("System"))
codeOutputTextBox.pack(side=BOTTOM, fill=X)



window.mainloop()

