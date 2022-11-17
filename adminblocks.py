import pandas as pd

import sqlite3
import tkinter as tk
from tkinter.ttk import *
import tkinter.messagebox
from globaldb import CreationDB


mainlistblock = ["C Chasse", "C SportCo", "D Glisse", "D Running", "E Rando/Camp", "Prio E", "V Cycle/Urban", "Prio V", "PFECA", "Implant"]
class Blocks(tk.Frame):
    
    statusconfig = False

    def __init__(self, master):
        
        self.master = master
        self.blocdataframe()
        self.show_block()


    def show_block(self):
        self.blocks_list.delete(0, tk.END)
        for block in mainlistblock:
            self.blocks_list.insert(tk.END, block)

    def blocdataframe(self):

        self.blocks_text = tk.StringVar()
        self.oldblocks_text = tk.StringVar()
        self.newblocks_text = tk.StringVar()

        self.intro_label = tk.Label(self.master, text="Configuration Activite", justify='center',font=('bold', 20))
        self.text_label = Label(self.master, text="Pour ajouter, supprimer ou renommer les blocks,\nselectionner les.\nPuis valider votre liste de blocks.", font=16, padding=10)
        self.intro_label.grid(row=0, column=1, columnspan=3)
        self.text_label.grid(row=2, column=1, columnspan=3)
        
        self.listblocktitle = Label(self.master, text="Liste de Blocks", font=('bold', 16), padding=15)
        self.listblocktitle.grid(row=3, column=1, pady=15)
        self.blocks_list = tk.Listbox(self.master, height=10, width=13, font=18) #, selectmode= "multiple"
        self.blocks_list.place(x=10,y=155) #padx=20, rowspan=3, columnspan=2 grid(row=4, column=1, pady=15)  #

        # Add Remove Blocks
        self.blocks_label = Label(self.master, text="Nom Block", justify='center', font=('bold', 14))
        self.blocks_label.place(x=203,y=165) #.grid(row=3, column=2)
        
        self.blocks_entry = tk.Entry(self.master, textvariable=self.blocks_text)
        self.blocks_entry.grid(row=4, column=2)

        self.add_btn = Button(self.master, text="Ajouter Block", bootstyle="success", width=12, command=self.add_block)
        self.add_btn.grid(row=6, column=2, pady=5)

        self.remove_btn = Button(self.master, text="Supprimer Block", bootstyle="warning", width=12, command=self.remove_block)
        self.remove_btn.grid(row=7, column=2, pady=10)

        # SEPARATOR PART
        
        # self.addsuppsep = Separator(self.master, bootstyle="success")
        # self.addsuppsep.grid(row=8, column=1, sticky="nsew", rowspan=2, columnspan=9)

        self.renomsep = Separator(self.master, bootstyle="success")
        self.renomsep.grid(row=15, column=1, sticky="nsew", rowspan=2, columnspan=9)

        # Changing Block
        self.oldblocks_label = tk.Label(self.master, text="Ancien Nom Block\n(à sélectionner)", justify='center', font=16)
        self.oldblocks_label.grid(row=11, column=1, pady=40)

        self.newblocks_label = tk.Label(self.master, text="Nouveau Nom Block", justify='center', font=16)
        self.newblocks_label.grid(row=13, column=1)

        self.oldblocks_entry = tk.Entry(self.master, textvariable=self.oldblocks_text)
        self.oldblocks_entry.grid(row=11, column=2)

        self.newblocks_entry = tk.Entry(self.master, textvariable=self.newblocks_text)
        self.newblocks_entry.grid(row=13, column=2)

        self.rename_btn = Button(self.master, text="Renommer Block", bootstyle="info", width=12,command=self.replace_block)
        self.rename_btn.grid(row=14, column=2, pady=10)

        # Bind select
        self.blocks_list.bind('<<ListboxSelect>>', self.select_item)       

    def add_block(self):
        if self.blocks_text.get() == '':
            tkinter.messagebox.showerror(
                "Champs requis", "Selectionnez un nom de la liste, svp")
            return
        else:
            mainlistblock.append(self.blocks_text.get())
        self.clear_text()
        self.show_block()

    def remove_block(self):
        if self.blocks_text.get() == '':
            tkinter.messagebox.showerror(
                "Champs requis", "Selectionnez un nom de la liste, svp")
            return
        else:
            self.indexit = mainlistblock.index(self.blocks_text.get())
            mainlistblock.pop(self.indexit)

        self.clear_text()
        self.show_block()

    def replace_block(self):
        if self.oldblocks_text.get() == '' or self.newblocks_text.get() == '':
            tkinter.messagebox.showerror(
                "Champs requis, Ancien nom ou Nouveau nom à remplir, svp.")
            return

        self.indexold = mainlistblock.index(self.oldblocks_text.get())
        mainlistblock[self.indexold] = self.newblocks_text.get()
        self.clear_text()
        self.show_block()

    def iniblock(self, listofblock):
        self.listofblock = listofblock
        for data in self.listofblock:
            
            self.pdb.insert_nameblock(self.listofblock.index(data)+1, "{}".format(data))     


    def lisfofblock(self):
        return mainlistblock

    
    def validate_block(self):
        global mainlistblock
        self.listofids = list(mainlistblock.index(x) for x in mainlistblock)
        #self.data = {'id': self.listofids, 'name': mainlistblock}
        #self.df = pd.DataFrame(self.data, columns=['id','name'])
        self.pdb = CreationDB(len(mainlistblock),"./database/goatdata.db")
        
        self.iniblock(mainlistblock)

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
