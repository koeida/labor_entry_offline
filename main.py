from tkinter import *
from tkinter.ttk import *
from collections import namedtuple

LaborSheetRow = namedtuple("LaborSheetRow", "area debit credit amount")

names = ["Keegan", "Adder", "Megan", "Saoirse", "Stephan", "Brittany"]
areas = ["DAIRY", "QUOTA", "GDN", "TOFU"]
areas.sort()

cur_area_typing = ""

def type_area(key,w):
    k = key.keysym.upper()
    if k in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
        new_typing = cur_area_typing + k
        # YOU ARE HERE. FILTER/FIRST THE AREAS LIST
        print(k)

class LaborSheetForm():
    def __init__(self, master, num_rows=10):
        Label(master, text="Area").grid(row=0, column=0, sticky=W)
        Label(master, text="Debit").grid(row=0, column=1, sticky=W)
        Label(master, text="Credit").grid(row=0, column=2, sticky=W)
        Label(master, text="Amount").grid(row=0, column=3, sticky=W)
        for i in range(num_rows):
            self.area = Entry(master, text="")
            self.area.state(["readonly"])
            self.area.bind('<KeyPress>', lambda k, x=self.area: type_area(k,x))
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
