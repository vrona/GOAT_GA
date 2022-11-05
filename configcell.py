import pandas as pd
import sqlite3
import tkinter as tk
import tkinter.messagebox
from tkinter import ttk

from ttkbootstrap import Style
from ttkbootstrap.constants import *
import datetime

class Configtab(tk.Frame):

    def __init__(self, master): 
        super().__init__(master)
        self.master = master

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
            # self.part_entry.delete(0, tk.END)
            # self.part_entry.insert(tk.END, self.selected_item[1])

        except IndexError:
            pass

    def configwidget(self, selecttab):

        self.selecttab = selecttab
        # Navigation Button
        self.navbutton = ttk.Button(self.master, text="Gestion Activite", bootstyle="PRIMARY", command=self.selecttab).grid(row=14, column=12, pady=10)

        # Checkbox Buttons Manuel vs Automation
        self.manualbutton = ttk.Checkbutton(self.master, text="Manual", bootstyle="warning-round-toggle").grid(row=10, column=12, pady=10)
        self.autopilotbutton = ttk.Checkbutton(self.master, text="AutoPilot", bootstyle="disabled-round-toggle").grid(row=12, column=12, pady=10)

        # Spinbox Button for Shifts
        self.shift_text = tk.StringVar()
        self.shift_text.set("Morning" "Afternoon" "Night")
        self.shiftbutton = ttk.Spinbox(self.master, text="Shift", bootstyle="PRIMARY", textvariable=self.shift_text).grid(row=2, column=2, pady=10)

        # Blocks list (listbox)
        self.blocks_list = tk.Listbox(self.master, height=8, width=50, border=0)
        self.blocks_list.grid(row=8, column=0, pady=20, padx=20, rowspan=3, columnspan=2) # , 
        # Create scrollbar
        self.scrollbar = ttk.Scrollbar(self.master, bootstyle="PRIMARY-round")
        self.scrollbar.grid(row=8, column=2)
        # Set scrollbar to parts
        self.blocks_list.configure(yscrollcommand=self.scrollbar.set)
        self.scrollbar.configure(command=self.blocks_list.yview)
        # Bind select
        self.blocks_list.bind('<<ListboxSelect>>', self.select_item)


"""
TAB "CONFIG"

Helps GA to configure its cell picking

How many blocks
What names
Then, delete or update number of blocks and names
One shot shift or long terms

Morning Shift
Afternoon Shift
Night Shift

"""