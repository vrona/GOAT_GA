import pandas as pd
import sqlite3
import tkinter as tk
import tkinter.messagebox
from tkinter import ttk

from gauge import Meter
from ttkbootstrap import Style
from ttkbootstrap.constants import *
import datetime

class Configtab(tk.Frame):

    def __init__(self, master): 
        super().__init__(master)
        self.master = master
    
    def configwidget(self):
        # Navigation Button
        self.navbutton = ttk.Button(self.master, text="Gestion Activite", bootstyle="PRIMARY", command=self.selecttab).grid(row=14, column=12, pady=10)
        self.manualbutton = ttk.Checkbutton(self.master, text="Manual", bootstyle="warning-round-toggle").grid(row=12, column=10, pady=10)
        self.autopilotbutton = ttk.Checkbutton(self.master, text="AutoPilot", bootstyle="disabled-round-toggle").grid(row=12, column=12, pady=10)

        # Blocks list (listbox)
        self.blocks_list = tk.Listbox(self.master, height=8, width=50, border=0)
        self.blocks_list.grid(row=2, column=4, pady=20, padx=20) #columnspan=2, rowspan=3, 
        # Create scrollbar
        self.scrollbar = tk.Scrollbar(self.master)
        self.scrollbar.grid(row=2, column=2)
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