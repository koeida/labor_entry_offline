from tkinter import *
from tkinter.commondialog import Dialog
from tkinter.ttk import *
from tkinter.messagebox import showerror
from collections import namedtuple
import json
import datetime
import sys

import tkinter as tk
import os
from misc import *
from sync import *


names = json.loads(open("sync_members.html","r").read())
areas = json.loads(open("sync_areas.html","r").read())
areas = names + areas
areas.sort()

#names = ["Keegan", "Adder", "Megan", "Saoirse", "Stephan", "Brittany"]
#names.sort()
#areas = ["DAIRY", "QUOTA", "GDN", "TOFU", "TOFU BOD"]
#areas.sort()

MEMBER_WIDTH = 40
cur_week = get_most_recent_week("weeks")
BLACK = "#000000"
RED = "#ff0000"


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
    if cur_week not in get_dirs(path):
        os.mkdir(path + cur_week) 

    # Write the labor sheet to file
    csv = to_csv(rows)
    file_name = cur_member_label["text"].strip()
    file_path = path + cur_week + "/%s.csv" % file_name
    with open(file_path, "w") as f:
        print(csv, file=f)

def get_sheet_list(path):
    """Get all sheets in current week"""
    sheet_files = os.listdir(path)
    sheet_files = filter(lambda f: f.endswith(".csv"), sheet_files)
    sheet_files = list(sheet_files)
    sheet_files.sort()
    return sheet_files

def get_next_sheet(cur_name, dirmod):
    path = "./weeks/" + cur_week

    sheet_files = get_sheet_list(path)

    # Calculate next index based on dirmod
    if cur_name == "":
        return sheet_files[0]
    else:
        cur_index = sheet_files.index(cur_name + ".csv")
        next_index = cur_index + dirmod 
        next_index = next_index if next_index >= 0 and next_index < len(sheet_files) else cur_index

        return sheet_files[next_index]

def move_sheet(cur_name, dirmod):
    cur_name = cur_name.strip()
    save(pwd.rows)
    if not validate_sheet(pwd, areas):
        showerror(message="Invalid sheet!")
        return None
    path = "./weeks/" + cur_week
    sheets = get_sheet_list(path)
    s = get_next_sheet(cur_name, dirmod)
    name, rows = load_sheet(s)
    display_sheet(name,rows)

    if sheets.index(s) > 0:
        prev_button["state"] = ACTIVE
    else:
        prev_button["state"] = DISABLED

    if sheets.index(s) < (len(sheets) - 1) :
        next_button["state"] = ACTIVE
    else:
        next_button["state"] = DISABLED


def load_sheet(fname):
    path = "./weeks/" + cur_week 
    lines = open(path + ("/%s" % fname)).readlines()
    lines = filter(lambda l: l.strip() != "",lines)
    lines = map(lambda l: l.strip().split(","), lines)
    lines = list(lines)
    member_name = fname[:-4]
    return (member_name, lines)

def initialize_form(member):
    for r in pwd.rows:
        for element in r:
            element["state"] = ACTIVE
            element["state"] = "!readonly"
            element.cur_index = 0
            element.cur_typing = ""
            element.delete(0,100)

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
    
        path = "./weeks/" + cur_week
        sheet_files = get_sheet_list(path)
        cur_names = list(map(lambda f: f[:-4], sheet_files))
        choices = filter(lambda n: n not in cur_names, names)
        choices = list(choices)

        self.mselect = Combobox(tf,state="readonly", values=choices)
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
        initialize_form(self.mselect.get().center(MEMBER_WIDTH))
        save(pwd.rows)

def load_all_sheets(cur_week):
    sheets = get_sheet_list("./weeks/%s" % cur_week)
    sheets = map(load_sheet, sheets)
    sheets = map(lambda s: {"member": s[0], "sheet":s[1]}, sheets)
    sheets = list(sheets)

    #year, month, day = list(map(int,cur_week.split("_")))
    #labor_week = datetime.date(year, month, day)
    return {"labor_week": cur_week, "sheets": sheets}

if len(sys.argv) == 1:
    root = Tk()
    root.option_add('*font',("sans", 24, ""))
    root.title("Offline labor sheet entry")

    mbar = Frame(root, relief=RAISED, borderwidth=2)
    mbar.pack(fill=X)
    top_frame = Frame(root)
    prev_button = Button(top_frame, text="<-", state=DISABLED)
    prev_button.pack(side=LEFT)
    cur_member_label = Label(top_frame, text="".center(MEMBER_WIDTH), relief=SUNKEN, justify=CENTER)
    cur_member_label.pack(side=LEFT, padx=5, pady=10)
    prev_button.bind("<ButtonPress>", lambda x: move_sheet(cur_member_label["text"],-1))
    next_button = Button(top_frame, text="->", state=DISABLED)
    next_button.pack(side=LEFT)
    next_button.bind("<ButtonPress>", lambda x: move_sheet(cur_member_label["text"],1))

    sheet_frame = Frame(root)
    pwd = LaborSheetForm(sheet_frame)

    fileBtn = Button(mbar, text="New Sheet", underline=0)
    fileBtn.bind("<ButtonPress>", lambda x: MemberDialog(root))
    fileBtn.pack(side=LEFT)

    syncBtn = Button(mbar, text="Sync to LaborDB", underline=0)
    syncBtn.bind("<ButtonPress>", lambda x: sync_sheets(load_all_sheets(cur_week)))
    syncBtn.pack(side=LEFT)

    top_frame.pack()
    sheet_frame.pack()

    sheets = get_sheet_list("./weeks/%s" % cur_week)
    if(len(sheets) > 0):
        member, rows = load_sheet(sheets[0])
        display_sheet(member, rows)
        if len(sheets) > 1:
            next_button["state"] = ACTIVE
    root.mainloop()
elif sys.argv[1] == "sync":
    sync_sheets(load_all_sheets(cur_week))
