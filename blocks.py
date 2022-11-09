import pandas as pd
import sqlite3
import tkinter as tk
from tkinter import ttk
import tkinter.messagebox


listofoutdoor = ["C Chasse", "C SportCo", "D Glisse", "D Running", "PFECA", "Implant"]
listofhopside = ["Bloc E", "Prio E", "Bloc E", "Prio V", "PFECA", "Implant"]

class Blocks:
    
    def __init__(self, master):
        self.master = master
        self.listofoutdoor = ["C Chasse", "C SportCo", "D Glisse", "D Running", "PFECA", "Implant"]
        self.listofhopside = ["Bloc E", "Prio E", "Bloc E", "Prio V", "PFECA", "Implant"]
        # Init selected item var
        self.selected_item = 0

        self.blocdataframe()
        self.show_block()

    def show_block(self):
        self.blocks_list.delete(0, tk.END)
        for block in self.listofoutdoor:
            self.blocks_list.insert(tk.END, block)

    def blocdataframe(self):

        self.blocks_text = tk.StringVar()
        self.oldblocks_text = tk.StringVar()
        self.newblocks_text = tk.StringVar()

        self.blocks_label = tk.Label(self.master, text="Nom Block", justify='center', font=16)
        self.blocks_label.grid(row=1, column=1)
        
        self.blocks_entry = tk.Entry(self.master, textvariable=self.blocks_text)
        self.blocks_entry.grid(row=1, column=2)

        self.blocks_list = tk.Listbox(self.master, height=len(self.listofoutdoor), width=15)
        self.blocks_list.place(x=555,y=10) #.grid(row=4, column=7, pady=20, padx=20, rowspan=3, columnspan=2)

        self.add_btn = ttk.Button(self.master, text="Ajouter Block", bootstyle="success", width=12, command=self.add_block)
        self.add_btn.grid(row=4, column=1, pady=20)

        self.remove_btn = ttk.Button(self.master, text="Supprimer Block", bootstyle="warning", width=12, command=self.remove_block)
        self.remove_btn.grid(row=4, column=3)

        # Changing Block
        self.oldblocks_text = tk.Label(self.master, text="Ancien Nom Block", justify='center', font=16)
        self.oldblocks_text.grid(row=6, column=1)

        self.newblocks_text = tk.Label(self.master, text="Nouveau Nom Block", justify='center', font=16)
        self.newblocks_text.grid(row=7, column=1)

        self.oldblocks_entry = tk.Entry(self.master, textvariable=self.oldblocks_text)
        self.oldblocks_entry.grid(row=6, column=3)

        self.newblocks_entry = tk.Entry(self.master, textvariable=self.newblocks_text)
        self.newblocks_entry.grid(row=8, column=3)

        self.rename_btn = ttk.Button(self.master, text="Renommer Block", bootstyle="info", width=12, command=self.replace_block)
        self.rename_btn.grid(row=10, column=1)

        # Bind select
        self.blocks_list.bind('<<ListboxSelect>>', self.select_item)


    def add_block(self):
        self.listofoutdoor.insert(0,self.blocks_text.get())
        self.clear_text()
        self.show_block()

    def remove_block(self):
        self.listofoutdoor.remove(self.blocks_text.get())
        self.clear_text()
        self.show_block()

    def replace_block(self):

        self.indexold = self.listofoutdoor.index(self.oldblocks_text.get())
        self.listofoutdoor.remove(self.blocks_text.get())
        self.listofoutdoor[self.indexold] = self.newblocks_text
        self.clear_text()
        self.show_block()

    def clear_text(self):
        self.blocks_entry.delete(0, tk.END)

    def select_item(self, event):
        # # Create global selected item to use in other functions
        # global self.selected_item
        try:
            # Get index
            index = self.blocks_list.curselection()[0]
            # Get selected item
            self.selected_item = self.blocks_list.get(index)
            # print(selected_item) # Print tuple

            # Add text to entries
            self.blocks_entry.delete(0, tk.END)
            self.blocks_entry.insert(tk.END, self.selected_item[1])
            self.oldblocks_entry.delete(0, tk.END)
            self.oldblocks_entry.insert(tk.END, self.selected_item[2])
        except IndexError:
            pass

        """
        # Create scrollbar
        self.scrollbar = ttk.Scrollbar(self.master, bootstyle="PRIMARY-round")
        self.scrollbar.grid(row=8, column=2)
        # Set scrollbar to parts
        self.blocks_list.configure(yscrollcommand=self.scrollbar.set)
        self.scrollbar.configure(command=self.blocks_list.yview)


        # self.listofids = list(self.listofblocks.index(x) for x in self.listofblocks)
        # self.data = {'id': self.listofids, 'name': self.listofblocks}
        # self.df = pd.DataFrame(self.data, columns=['id','name'])
        # return self.df.to_string()
        """


# bloc = Blocks()
# bloc.blocdataframe()