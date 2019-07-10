from tkinter import *
from collections import namedtuple

LaborSheetRow = namedtuple("LaborSheetRow", "area debit credit amount")


class LaborSheetForm():
    def __init__(self, master, num_rows=10):
        self.rows = [LaborSheetRow("", 0, 0, 0) for x in range(num_rows)] 
        Label(master, text="Area").grid(row=0, column=0, sticky=W)
        Label(master, text="Debit").grid(row=0, column=1, sticky=W)
        Label(master, text="Credit").grid(row=0, column=2, sticky=W)
        Label(master, text="Amount").grid(row=0, column=3, sticky=W)
        for i in range(num_rows):
            Entry(master, width=8).grid(row=i+1, column=0, sticky=W)
            Entry(master, width=8).grid(row=i+1, column=1, sticky=W)
            Entry(master, width=8).grid(row=i+1, column=2, sticky=W)
            Entry(master, width=8).grid(row=i+1, column=3, sticky=W)

root = Tk()
pwd = LaborSheetForm(root)
root.mainloop()
