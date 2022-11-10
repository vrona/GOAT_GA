import tkinter as tk
import tkinter.messagebox
from tkinter import ttk


class Tabs(tk.Frame):

    def __init__(self, master): #tabcontrol, , listofcell
        super().__init__(master)
        self.master = master
        # self.tabcontrol.title("GOAT Of GA (alpha)")
        # self.tabcontrol.geometry("1600x1080")
        # #self.tabcontrol = self.tabcontrol
        self.tabcontrol = ttk.Notebook(self.master)
        self.tabcontrol.grid(pady=5)

        #self.listoftabs = list(self.config, self.activity, self.reporting, self.admin, self.credit)

    def credittab(self):
        # self.tabcontrol = tabcontrol
        self.credit = tk.Frame(self.tabcontrol, width= 1600, height=1080)
        self.credit.pack(fill="both", expand=1)
        self.tabcontrol.add(self.credit, text="Credits")

    def configtab(self):
        # self.tabcontrol = tabcontrol
        self.config = tk.Frame(self.tabcontrol, width= 1600, height=1080)
        self.config.pack(fill="both", expand=1)
        self.tabcontrol.add(self.config, text="Config")

    def activitytab(self):
        # self.tabcontrol = tabcontrol
        self.activity = tk.Frame(self.tabcontrol, width= 1600, height=1080)
        self.activity.pack(fill="both", expand=1)
        self.tabcontrol.add(self.activity, text="Activite")

    def reportingtab(self):
        # self.tabcontrol = tabcontrol
        self.reporting = tk.Frame(self.tabcontrol, width= 1600, height=1080)
        self.reporting.pack(fill="both", expand=1)
        self.tabcontrol.add(self.reporting, text="Reporting")

    def admintab(self):
        # self.tabcontrol = tabcontrol
        self.admin = tk.Frame(self.tabcontrol, width= 1600, height=1080)
        self.admin.pack(fill="both", expand=1)
        self.tabcontrol.add(self.admin, text="Admin")
        

    def selecttab(self, tab):
        self.tab = tab
        self.tabcontrol.select(self.tab)