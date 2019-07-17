from tkinter import *
from tkinter.commondialog import Dialog
from tkinter.ttk import *
from tkinter.messagebox import showerror
from collections import namedtuple

import tkinter as tk
import os


names = ["Keegan", "Adder", "Megan", "Saoirse", "Stephan", "Brittany"]
names.sort()
areas = ["DAIRY", "QUOTA", "GDN", "TOFU", "TOFU BOD"]
areas.sort()

MEMBER_WIDTH = 40
CUR_WEEK = "test"
BLACK = "#000000"
RED = "#ff0000"

def get_dirs(path):
    dirs = []
    with os.scandir(path) as it:
        dirs = filter(lambda i: i.is_dir(), it)
        dirs = map(lambda i: i.name, dirs)
        dirs = list(dirs)
    return dirs

def valid_type(type_func, v):
    try:
        type_func(v)
        return True
    except:
        return False

def update_area_box(box, match):
    box.state(["!readonly"])
    box.delete(0,100)
    if match != None:
        box.insert(0,box.cur_typing)
        area_insert_start = len(box.cur_typing)
        area_insert = match[len(box.cur_typing):]
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
    k = key.keysym.upper()
    k = " " if k == "SPACE" else k
    w.cur_index, w.cur_typing = area_input(k, w.cur_index,  w.cur_typing)
    match = get_match(w.cur_index, w.cur_typing)

    update_area_box(w, match)

def area_lose_focus(event):
    event.widget.select_clear()
    area_name = event.widget.get()
    event.widget.cur_typing = area_name
    event.widget.cur_index = 0
    validate_sheet(pwd, areas)
    save(pwd.rows)

def get_row(r):
    debit = r[0].get()
    credit = r[1].get() 
    amount = r[2].get()

    return (debit, credit, amount)

def valid_row(debit, credit, amount, areas):
    return (debit in areas) and (credit in areas) and valid_type(float,amount) 

def to_csv(rows):
    csvrows = map(get_row, rows)
    csvrows = filter(lambda r: valid_row(*r, areas), csvrows)
    csvrows = map(lambda r: ",".join(r), csvrows)
    csvrows = "\n".join(csvrows)
    return csvrows

def validate_sheet(sheet, areas):
    def mark_entry_invalid(e):
        e["foreground"] = RED 
        e.state(["!readonly"])
        e.delete(0,100)
        e.insert(0,"***INVALID***")
        e.state(["readonly"])

    rows = filter(lambda r: get_row(r) != ("", "", ""), sheet.rows)
    success = True
    for r in rows:
        debit, credit, amount = (r[0], r[1], r[2])
        debit["foreground"] = BLACK
        if debit.get() not in areas:
            mark_entry_invalid(debit)
            success = False

        credit["foreground"] = BLACK
        if credit.get() not in areas:
            mark_entry_invalid(credit)
            success = False

        amount["foreground"] = BLACK 
        if not valid_type(float,amount.get()):
            amount["foreground"] = RED 
            success = False
    return success

def area_get_focus(e):
    e.widget["foreground"] = BLACK
    e.widget.state(["!readonly"])
    e.widget.delete(0,100)
    e.widget.insert(0,e.widget.cur_typing)
    e.widget.state(["readonly"])

def amount_get_focus(e):
    e.widget["foreground"] = BLACK

def amount_lose_focus(e):
    validate_sheet(pwd, areas)
    save(pwd.rows)

def save(rows):
    # Create folders if necessary based on week name
    if "weeks" not in get_dirs("."):
        os.mkdir("weeks")

    path = "./weeks/"
    if CUR_WEEK not in get_dirs(path):
        os.mkdir(path + CUR_WEEK) 

    # Write the labor sheet to file
    csv = to_csv(rows)
    file_name = cur_member_label["text"].strip()
    with open(path + CUR_WEEK + "/%s.csv" % file_name, "w") as f:
        print(csv, file=f)

def get_next_sheet(cur_name, dirmod):
    path = "./weeks/" + CUR_WEEK

    # Get all sheets in current week
    sheet_files = os.listdir(path)
    sheet_files = filter(lambda f: f.endswith(".csv"), sheet_files)
    sheet_files = list(sheet_files)
    sheet_files.sort()

    # Calculate next index based on dirmod
    cur_index = sheet_files.index(cur_name + ".csv")
    next_index = cur_index + dirmod 
    next_index = next_index if next_index >= 0 and next_index < len(sheet_files) else cur_index

    return sheet_files[next_index]

def move_sheet(cur_name, dirmod):
    save(pwd.rows)
    get_next_sheet(cur_index, dirmod)

def load_sheet(fname):
    path = "./weeks/" + CUR_WEEK 
    lines = open(path + ("/%s.csv" % fname)).readlines()
    lines = map(lambda l: l.strip().split(","), lines)
    lines = list(lines)
    return (fname, lines)

def initialize_form(member):
    for r in pwd.rows:
        for element in r:
            element["state"] = ACTIVE
        r[0]["state"] = "readonly"
        r[1]["state"] = "readonly"
    cur_member_label["width"] = 0
    cur_member_label["text"] = member


def display_sheet(member, rows):
    initialize_form(member)
    for i in range(len(rows)):
        cur_form_row = pwd.rows[i]
        debit, credit, amount = rows[i]
        
        cur_form_row[0]["state"] = "!readonly"
        cur_form_row[1]["state"] = "!readonly"

        cur_form_row[0].delete(0,1000)
        cur_form_row[0].insert(0,debit)
        cur_form_row[1].delete(0,1000)
        cur_form_row[1].insert(0,credit)
        cur_form_row[2].delete(0,1000)
        cur_form_row[2].insert(0,amount)

        cur_form_row[0]["state"] = "readonly"
        cur_form_row[1]["state"] = "readonly"

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
            debit.bind('<FocusIn>', area_get_focus, "")
            debit.bind('<FocusOut>', area_lose_focus, "")
            debit.grid(row=i+1, column=0, sticky=W, padx=padding, pady=padding)
            debit.cur_index = 0
            debit.cur_typing = ""

            credit = Entry(master, state=DISABLED)
            credit.bind('<KeyPress>', lambda k, x=credit: type_area(k,x), "")
            credit.bind('<FocusIn>', area_get_focus, "")
            credit.bind('<FocusOut>', area_lose_focus, "")
            credit.grid(row=i+1, column=1, sticky=W, padx=padding, pady=padding)
            credit.cur_index = 0
            credit.cur_typing = ""

            amount = Entry(master, width=8, state=DISABLED)
            amount.grid(row=i+1, column=2, sticky=W, padx=padding, pady=padding)
            amount.bind('<FocusOut>', amount_lose_focus)
            amount.bind('<FocusIn>', amount_get_focus, "")
            self.rows.append((debit,credit,amount))

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
            r[1]["state"] = "readonly"
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
saveBtn.bind("<ButtonPress>", lambda x: save(pwd.rows))
saveBtn.pack(side=LEFT)

top_frame.pack()
sheet_frame.pack()

member, rows = load_sheet("Adder")
display_sheet(member, rows)
root.mainloop()
