from tkinter import *
from tkinter.commondialog import Dialog
from tkinter.ttk import *
from collections import namedtuple

import tkinter as tk

LaborSheetRow = namedtuple("LaborSheetRow", "debit credit amount")
LaborSheet = namedtuple("LaborSheet", "name rows")

names = ["Keegan", "Adder", "Megan", "Saoirse", "Stephan", "Brittany"]
names.sort()
areas = ["DAIRY", "QUOTA", "GDN", "TOFU", "TOFU BOD"]
areas.sort()

MEMBER_WIDTH = 40
CUR_WEEK = "test"

cur_debit_typing = ""
cur_debit_index = 0

def update_area_box(box, typing, match):
    box.state(["!readonly"])
    box.delete(0,100)
    if match != None:
        box.insert(0,typing)
        area_insert_start = len(typing)
        area_insert = match[len(typing):]
        box.insert(area_insert_start, area_insert)
        box.selection_range(area_insert_start, area_insert_start + len(area_insert))
    box.state(["readonly"])

def get_match(cur_index, t):
    matches = get_matches(t) 
    if len(t) > 0 and matches != []:
        return matches[cur_index]
    else:
        return None

def get_matches(t):
    if len(t) == 0:
        return []
    else:
        matches = list(filter(lambda a: a.startswith(t), areas))
        return matches 

def area_input(k, cur_index, cur_typing):
    def alpha(cur_index, cur_typing, k=k):
        new_typing = cur_typing + k
        matches = get_matches(new_typing)
        typing = cur_typing if len(matches) == 0 else new_typing
        return (cur_index, typing)
    def backspace(cur_index, cur_typing):
        new_typing = cur_typing[:-1]
        new_index = 0 if len(new_typing) == 0 else cur_index
        return (new_index, new_typing)
    def downup(cur_index, cur_typing, d):
        matches = get_matches(cur_typing)
        imod = cur_index + d 
        valid_index = imod < len(matches) and imod >= 0 and matches != [] 
        new_index = imod if valid_index else cur_index
        return (new_index, cur_typing)

    if k in "ABCDEFGHIJKLMNOPQRSTUVWXYZ ":
        return alpha(cur_index, cur_typing)
    elif k == "BACKSPACE":
        return backspace(cur_index, cur_typing)
    elif k == "DOWN":
        return downup(cur_index, cur_typing, 1)
    elif k == "UP":
        return downup(cur_index, cur_typing, -1)
    else:
        return (cur_index, cur_typing)

def type_area(key,w):
    global cur_debit_typing, cur_debit_index

    k = key.keysym.upper()
    k = " " if k == "SPACE" else k
    cur_debit_index, cur_debit_typing = area_input(k, cur_debit_index,  cur_debit_typing)
    match = get_match(cur_debit_index, cur_debit_typing)

    update_area_box(w, cur_debit_typing, match)

def area_get_focus(event):
    #set cur_index to end of area name
    #set cur_typing to entire text
    pass

def area_lose_focus(event):
    global cur_debit_index, cur_debit_typing
    event.widget.select_clear()
    cur_debit_index = 0
    cur_debit_typing = ""


class LaborSheetForm():
    def __init__(self, master, num_rows=10):
        Label(master, text="Debit").grid(row=0, column=0, sticky=W)
        Label(master, text="Credit").grid(row=0, column=1, sticky=W)
        Label(master, text="Amount").grid(row=0, column=2, sticky=W)
        padding = 2
        self.rows = []
        for i in range(num_rows):
            debit = Entry(master, state=DISABLED)
            debit.state(["readonly"])
            debit.bind('<KeyPress>', lambda k, x=debit: type_area(k,x), "")
            debit.bind('<FocusOut>', area_lose_focus, "")
            debit.bind('<FocusIn>', area_get_focus, "")
            debit.grid(row=i+1, column=0, sticky=W, padx=padding, pady=padding)
            credit = Entry(master, width=8, state=DISABLED)
            credit.grid(row=i+1, column=1, sticky=W, padx=padding, pady=padding)
            amount = Entry(master, width=8, state=DISABLED)
            amount.grid(row=i+1, column=2, sticky=W, padx=padding, pady=padding)
            self.rows.append((debit,credit,amount))
    def save(self):
        def get_row(r):
            debit = r[0].get()
            credit = r[1].get() # wrong needs to be an entry field
            amount = r[2].get()

            return (debit, credit, amount)
            
        sheet_rows = [LaborSheetRow(*get_row(r)) for r in self.rows if get_row(r) != ("","","")]
        sheet = LaborSheet(cur_member_label["text"].strip(), sheet_rows)

class MemberDialog(Dialog):
    def __init__(self, master):
        self.root = Toplevel(master)
        self.root.title("Select member name  ")

        tf = Frame(self.root)
        Label(tf, text="Member:").pack(side=LEFT, padx=5)
        self.mselect = Combobox(tf,state="readonly", values=names)
        self.mselect.pack(side=LEFT, padx=5)
        self.mselect.current(0)
        tf.pack(pady=5)

        bf = Frame(self.root)
        Button(bf, text="Cancel").pack(side=LEFT, anchor=E, padx=5)
        add = Button(bf, text="Add")
        add.pack(side=LEFT, anchor=E)
        add.bind("<Button-1>", lambda x: self.ok(master))
        bf.pack(anchor=E, pady=5, padx=5)

        self.root.transient(master)
    def ok(self, master):
        for r in pwd.rows:
            for element in r:
                element["state"] = ACTIVE
            r[0]["state"] = "readonly"
        cur_member_label["width"] = 0
        cur_member_label["text"] = self.mselect.get().center(MEMBER_WIDTH)

root = Tk()
root.option_add('*font',("sans", 24, ""))
root.title("Offline labor sheet entry")

mbar = Frame(root, relief=RAISED, borderwidth=2)
mbar.pack(fill=X)
top_frame = Frame(root)
Button(top_frame, text="<-", state=DISABLED).pack(side=LEFT)
cur_member_label = Label(top_frame, text="".center(MEMBER_WIDTH), relief=SUNKEN, justify=CENTER)
cur_member_label.pack(side=LEFT, padx=5, pady=10)
Button(top_frame, text="->", state=DISABLED).pack(side=LEFT)

sheet_frame = Frame(root)
pwd = LaborSheetForm(sheet_frame)

fileBtn = Button(mbar, text="New Sheet", underline=0)
fileBtn.bind("<ButtonPress>", lambda x: MemberDialog(root))
fileBtn.pack(side=LEFT)
saveBtn = Button(mbar, text="Save Sheet", underline=0)
saveBtn.bind("<ButtonPress>", lambda x: pwd.save())
saveBtn.pack(side=LEFT)

top_frame.pack()
sheet_frame.pack()

root.mainloop()
