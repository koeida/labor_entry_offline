from tkinter import *
from tkinter.ttk import *
from collections import namedtuple

LaborSheetRow = namedtuple("LaborSheetRow", "area debit credit amount")

names = ["Keegan", "Adder", "Megan", "Saoirse", "Stephan", "Brittany"]
areas = ["DAIRY", "QUOTA", "GDN", "TOFU", "TOFU BOD"]
areas.sort()

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
        if len(matches) == 0:
            new_typing = cur_typing
        return (cur_index, new_typing)
    def backspace(cur_index, cur_typing):
        new_typing = cur_typing[:-1]
        new_index = 0 if len(new_typing) == 0 else cur_index
        return (new_index, new_typing)
    def down(cur_index, cur_typing):
        matches = get_matches(cur_typing)
        valid_index = len(matches) > 1 and cur_index < (len(matches) - 1)
        new_index = cur_index + 1 if valid_index else cur_index
        return (new_index, cur_typing)
    def up(cur_index, cur_typing):
        matches = get_matches(cur_typing)
        valid_index = len(matches) > cur_index and matches != [] 
        new_index = cur_index - 1 if valid_index else cur_index
        print(new_index)
        return (new_index, cur_typing)

    if k in "ABCDEFGHIJKLMNOPQRSTUVWXYZ ":
        return alpha(cur_index, cur_typing)
    elif k == "BACKSPACE":
        return backspace(cur_index, cur_typing)
    elif k == "DOWN":
        return down(cur_index, cur_typing)
    elif k == "UP":
        return up(cur_index, cur_typing)
    else:
        return (cur_index, cur_typing)

def type_area(key,w):
    global cur_area_typing, cur_area_index

    k = key.keysym.upper()
    k = " " if k == "SPACE" else k
    cur_area_index, cur_area_typing = area_input(k, cur_area_index,  cur_area_typing)
    match = get_match(cur_area_index, cur_area_typing)

    update_area_box(w, cur_area_typing, match)

class LaborSheetForm():
    def __init__(self, master, num_rows=10):
        Label(master, text="Area").grid(row=0, column=0, sticky=W)
        Label(master, text="Debit").grid(row=0, column=1, sticky=W)
        Label(master, text="Credit").grid(row=0, column=2, sticky=W)
        Label(master, text="Amount").grid(row=0, column=3, sticky=W)
        for i in range(num_rows):
            self.area = Entry(master)
            self.area.state(["readonly"])
            self.area.bind('<KeyPress>', lambda k, x=self.area: type_area(k,x), "")
            #self.area.bind('<KeyRelease>', lambda k, x=self.area: x.delete(len(cur_area_typing),1), "")
            self.area.grid(row=i+1, column=0, sticky=W)
            self.debit = Entry(master, width=8)
            self.debit.grid(row=i+1, column=1, sticky=W)
            self.credit = Entry(master, width=8)
            self.credit.grid(row=i+1, column=2, sticky=W)
            self.amount = Entry(master, width=8)
            self.amount.grid(row=i+1, column=3, sticky=W)

root = Tk()
root.option_add('*font',("sans", 24, ""))

top_frame = Frame(root)
Button(top_frame, text="<-").pack(side=LEFT)
Label(top_frame, text="Keegan").pack(side=LEFT)
Button(top_frame, text="->").pack(side=LEFT)


sheet_frame = Frame(root)
pwd = LaborSheetForm(sheet_frame)

top_frame.pack()
sheet_frame.pack()

root.mainloop()
