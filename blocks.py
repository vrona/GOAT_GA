import pandas as pd
import sqlite3
import tkinter as tk

listofoutdoor = ["C Chasse", "C SportCo", "D Glisse", "D Running", "PFECA", "Implant"]
listofhopside = ["Bloc E", "Prio E", "Bloc E", "Prio V", "PFECA", "Implant"]

class Blocks:
    
    def __init__(self, master):
        self.master = master


    def blocdataframe(self):
        listofoutdoor = ["C Chasse", "C SportCo", "D Glisse", "D Running", "PFECA", "Implant"]
        listofhopside = ["Bloc E", "Prio E", "Bloc E", "Prio V", "PFECA", "Implant"]

        self.blocks_text = tk.StringVar()
        self.blocks_label = tk.Label(self.master, text="Liste des Blocks", justify='center', font=16)
        self.blocks_label.grid(row=4, column=3)

        self.blocks_entry = tk.Entry(self.master, textvariable=self.blocks_text)
        self.blocks_entry.grid(row=4, column=5)

        # self.listofids = list(self.listofblocks.index(x) for x in self.listofblocks)
        # self.data = {'id': self.listofids, 'name': self.listofblocks}
        # self.df = pd.DataFrame(self.data, columns=['id','name'])
        # return self.df.to_string()


# bloc = Blocks()
# bloc.blocdataframe()