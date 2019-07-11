from tkinter import *
from tkinter.ttk import *
from collections import namedtuple

LaborSheetRow = namedtuple("LaborSheetRow", "area debit credit amount")

names = ["Keegan", "Adder", "Megan", "Saoirse", "Stephan", "Brittany"]
areas = ["DAIRY", "QUOTA", "GDN", "TOFU"]
areas.sort()

cur_area_typing = ""

def first(c,l):
    for x in l:
        if c(x):
            return x
    return None

def type_area(key,w):
    global cur_area_typing
    k = key.keysym.upper()
    w.state(["!readonly"])
    if k in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
        new_typing = cur_area_typing + k
        match = first(lambda a: a.startswith(new_typing), areas)
        w.delete(0,100)
        if match != None:
            print(w.selection_range.__doc__)
            cur_area_typing = new_typing

            w.insert(0,new_typing)
           
            area_insert_start = len(new_typing)
            area_insert = match[len(new_typing):]
            w.insert(area_insert_start, area_insert)
            w.selection_range(area_insert_start, area_insert_start + len(area_insert))
        else:
            w.insert(0,cur_area_typing)
    elif k == "BACKSPACE":
        cur_area_typing = cur_area_typing[:-1]
        w.delete(len(cur_area_typing) - 1,100)

    w.state(["readonly"])
            

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
