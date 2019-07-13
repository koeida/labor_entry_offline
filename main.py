from tkinter import *
from tkinter.ttk import *
from collections import namedtuple

import tkinter as tk

LaborSheetRow = namedtuple("LaborSheetRow", "area debit credit amount")

names = ["Keegan", "Adder", "Megan", "Saoirse", "Stephan", "Brittany"]
areas = ["DAIRY", "QUOTA", "GDN", "TOFU", "TOFU BOD"]
areas.sort()

MEMBER_WIDTH = 40

cur_area_typing = ""
cur_area_index = 0

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
    global cur_area_typing, cur_area_index

    k = key.keysym.upper()
    k = " " if k == "SPACE" else k
    cur_area_index, cur_area_typing = area_input(k, cur_area_index,  cur_area_typing)
    match = get_match(cur_area_index, cur_area_typing)

    update_area_box(w, cur_area_typing, match)

def area_get_focus(event):
    #set cur_index to end of area name
    #set cur_typing to entire text
    pass

def area_lose_focus(event):
    global cur_area_index, cur_area_typing
    event.widget.select_clear()
    cur_area_index = 0
    cur_area_typing = ""


class LaborSheetForm():
    def __init__(self, master, num_rows=10):
        Label(master, text="Area").grid(row=0, column=0, sticky=W)
        Label(master, text="Debit").grid(row=0, column=1, sticky=W)
        Label(master, text="Credit").grid(row=0, column=2, sticky=W)
        Label(master, text="Amount").grid(row=0, column=3, sticky=W)
        padding = 2
        self.rows = []
        for i in range(num_rows):
            area = Entry(master, state=DISABLED)
            area.state(["readonly"])
            area.bind('<KeyPress>', lambda k, x=area: type_area(k,x), "")
            area.bind('<FocusOut>', area_lose_focus, "")
            area.bind('<FocusIn>', area_get_focus, "")
            area.grid(row=i+1, column=0, sticky=W, padx=padding, pady=padding)
            debit = Entry(master, width=8, state=DISABLED)
            debit.grid(row=i+1, column=1, sticky=W, padx=padding, pady=padding)
            credit = Entry(master, width=8, state=DISABLED)
            credit.grid(row=i+1, column=2, sticky=W, padx=padding, pady=padding)
            amount = Entry(master, width=8, state=DISABLED)
            amount.grid(row=i+1, column=3, sticky=W, padx=padding, pady=padding)
            self.rows.append((area,debit,credit,amount))
    def new_sheet(self, member):
        for r in self.rows:
            for element in r:
                element["state"] = ACTIVE
            r[0]["state"] = "readonly"
        cur_member_label["width"] = 0
        cur_member_label["text"] = member.center(MEMBER_WIDTH)

        
        



root = Tk()
root.option_add('*font',("sans", 24, ""))

print(dir(tk))
#foo = ComboBoxDialog

mbar = Frame(root, relief=RAISED, borderwidth=2)
mbar.pack(fill=X)
top_frame = Frame(root)
Button(top_frame, text="<-").pack(side=LEFT)
cur_member_label = Label(top_frame, text="".center(MEMBER_WIDTH), relief=SUNKEN, justify=CENTER)
cur_member_label.pack(side=LEFT, padx=5, pady=10)
Button(top_frame, text="->").pack(side=LEFT)

sheet_frame = Frame(root)
pwd = LaborSheetForm(sheet_frame)

fileBtn = Button(mbar, text="New Sheet", underline=0)
fileBtn.bind("<ButtonPress>", lambda x: pwd.new_sheet("Keegan"))
fileBtn.pack(side=LEFT)

top_frame.pack()
sheet_frame.pack()

root.mainloop()
