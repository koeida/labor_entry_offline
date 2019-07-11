from tkinter import *
from tkinter.ttk import *
from collections import namedtuple

LaborSheetRow = namedtuple("LaborSheetRow", "area debit credit amount")

names = ["Keegan", "Adder", "Megan", "Saoirse", "Stephan", "Brittany"]
areas = ["DAIRY", "QUOTA", "GDN", "TOFU"]
areas.sort()

cur_area_typing = ""
cur_area_index = 0

def first(c,l):
    for x in l:
        if c(x):
            return x
    return None

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

def type_area(key,w):
    global cur_area_typing, cur_area_index
    k = key.keysym.upper()
    if k in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
        cur_area_index = 0
        new_typing = cur_area_typing + k
        matches = list(filter(lambda a: a.startswith(new_typing), areas))
        if len(matches) != 0:
            match = matches[0]
            cur_area_typing = new_typing
            update_area_box(w, new_typing, match)
    elif k == "BACKSPACE":
        cur_area_typing = cur_area_typing[:-1]
        if len(cur_area_typing) > 0:
            matches = list(filter(lambda a: a.startswith(cur_area_typing), areas))
            match = matches[cur_area_index]
        else:
            cur_area_index = 0
            match = None
        update_area_box(w, cur_area_typing, match)
    elif k == "DOWN":
        matches = list(filter(lambda a: a.startswith(cur_area_typing), areas))
        if len(mactches) > 1 and cur_area_index < len(matches):
            cur_area_index += 1

        print(k)

            

class LaborSheetForm():
    def __init__(self, master, num_rows=10):
        Label(master, text="Area").grid(row=0, column=0, sticky=W)
        Label(master, text="Debit").grid(row=0, column=1, sticky=W)
        Label(master, text="Credit").grid(row=0, column=2, sticky=W)
        Label(master, text="Amount").grid(row=0, column=3, sticky=W)
        for i in range(num_rows):
            self.area = Entry(master)
            self.area.state(["readonly"])
            #self.area.unbind_class("Entry", "<KeyPress>")
            self.area.bind('<KeyPress>', lambda k, x=self.area: type_area(k,x), "")
            self.area.bind('<KeyRelease>', lambda k, x=self.area: x.delete(len(cur_area_typing),1), "")
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
