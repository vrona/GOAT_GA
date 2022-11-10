import pandas as pd

import sqlite3
import tkinter as tk
from tkinter.ttk import *
import tkinter.messagebox

class Blocks(tk.Frame):
    
    statusconfig = False

    def __init__(self, master):
        self.master = master
        self.mainlistblock = ["C Chasse", "C SportCo", "D Glisse", "D Running", "PFECA", "Implant"]
        self.listofhopside = ["Bloc E", "Prio E", "Bloc E", "Prio V", "PFECA", "Implant"]
        self.blocdataframe()
        self.show_block()


    def show_block(self):
        self.blocks_list.delete(0, tk.END)
        for block in self.mainlistblock:
            self.blocks_list.insert(tk.END, block)

    def blocdataframe(self):
        style = Style()
        style.configure('valid.btn', font = (20, 'bold'), foreground ='red')

        self.blocks_text = tk.StringVar()
        self.oldblocks_text = tk.StringVar()
        self.newblocks_text = tk.StringVar()

        self.intro_label = tk.Label(self.master, text="Configuration Activite", justify='center',font=('bold', 20))
        self.text_label = Label(self.master, text="Pour ajouter, supprimer ou renommer les blocks,\nselectionner les.\nPuis valider votre liste de blocks.", font=16, padding=10)
        self.intro_label.grid(row=0, column=1, columnspan=3)
        self.text_label.grid(row=2, column=1, columnspan=3)
        
        self.listblocktitle = Label(self.master, text="Liste de Blocks", font=('bold', 16), padding=15)
        self.listblocktitle.grid(row=3, column=1, pady=15)
        self.blocks_list = tk.Listbox(self.master, height=len(self.mainlistblock), width=15, font=18)
        self.blocks_list.grid(row=4, column=1, pady=15)  #.place(x=555,y=10) #padx=20, rowspan=3, columnspan=2

        # Add Remove Blocks
        self.blocks_label = Label(self.master, text="Nom Block", justify='center', font=('bold', 16))
        self.blocks_label.grid(row=7, column=1)
        
        self.blocks_entry = tk.Entry(self.master, textvariable=self.blocks_text)
        self.blocks_entry.grid(row=7, column=2)

        self.add_btn = Button(self.master, text="Ajouter Block", bootstyle="success", width=12, command=self.add_block)
        self.add_btn.grid(row=9, column=1, pady=30)

        self.remove_btn = Button(self.master, text="Supprimer Block", bootstyle="warning", width=12, command=self.remove_block)
        self.remove_btn.grid(row=9, column=3)

        # Changing Block
        self.oldblocks_label = tk.Label(self.master, text="Ancien Nom Block", justify='center', font=16)
        self.oldblocks_label.grid(row=11, column=1)

        self.newblocks_label = tk.Label(self.master, text="Nouveau Nom Block", justify='center', font=16)
        self.newblocks_label.grid(row=13, column=1)

        self.oldblocks_entry = tk.Entry(self.master, textvariable=self.oldblocks_text)
        self.oldblocks_entry.grid(row=11, column=2, pady=10)

        self.newblocks_entry = tk.Entry(self.master, textvariable=self.newblocks_text)
        self.newblocks_entry.grid(row=13, column=2)

        self.rename_btn = Button(self.master, text="Renommer Block", bootstyle="info", width=12,command=self.replace_block)
        self.rename_btn.grid(row=14, column=1, pady=30)

        # Bind select
        self.blocks_list.bind('<<ListboxSelect>>', self.select_item)

        # Validate Block List
        
        self.validblock_btn = Button(self.master, text="Valider Blocks", style='valid.btn', width=12, command=self.validate_block)
        self.validblock_btn.grid(row=17, column=1)

    def add_block(self):
        self.mainlistblock.append(self.blocks_text.get())
        self.clear_text()
        self.show_block()

    def remove_block(self):
        self.indexit = self.mainlistblock.index(self.blocks_text.get())
        self.mainlistblock.pop(self.indexit)
        self.clear_text()
        self.show_block()

    def replace_block(self):

        self.indexold = self.mainlistblock.index(self.oldblocks_text.get())
        self.mainlistblock[self.indexold] = self.newblocks_text.get()
        self.clear_text()
        self.show_block()


    def validate_block(self):

        global statusconfig

        if self.validblock_var.get() == 1:
            statusconfig = True
            self.listofids = list(self.mainlistblock.index(x) for x in self.mainlistblock)
            self.data = {'id': self.listofids, 'name': self.mainlistblock}
            self.df = pd.DataFrame(self.data, columns=['id','name'])
            return self.mainlistblock

        else:
            statusconfig = False


    def clear_text(self):
        self.blocks_entry.delete(0, tk.END)
        self.oldblocks_entry.delete(0, tk.END)
        self.newblocks_entry.delete(0, tk.END)

    def select_item(self, event):

        try:
            # Get index
            index = self.blocks_list.curselection()
            # Get selected item
            self.selected_item = self.blocks_list.get(index)
            #print(self.selected_item)

            # Add text to entries
            self.blocks_entry.delete(0, tk.END)
            self.blocks_entry.insert(tk.END, self.selected_item)
            self.oldblocks_entry.delete(0, tk.END)
            self.oldblocks_entry.insert(tk.END, self.selected_item)
        except IndexError:
            pass

        """
        # Create scrollbar
        self.scrollbar = Scrollbar(self.master, bootstyle="PRIMARY-round")
        self.scrollbar.grid(row=8, column=2)
        # Set scrollbar to parts
        self.blocks_list.configure(yscrollcommand=self.scrollbar.set)
        self.scrollbar.configure(command=self.blocks_list.yview)
        """


# bloc = Blocks()
# bloc.blocdataframe()