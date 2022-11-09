import tkinter as tk
import pandas as pd
import tkinter.messagebox
from tkinter import ttk
from blocks import Blocks

from ttkbootstrap import Style
from ttkbootstrap.constants import *

class Configtab(tk.Frame):

    def __init__(self, master): 
        super().__init__(master)
        self.master = master


    def adminwidget(self):

        # Text
        self.text_intro = tk.Text(self.master, height=12, width= 40, border=0)
        self.text_intro.place(x=555,y=10)
        #self.text_intro.grid(row=10, column=10)
        self.text_itself = """Cher-e GA,\n\nAujourd'hui c'est ton jour ;-)\n\nConfigure ta gestion d'activité :\nQuel shift : Matin, Après-Midi, Nuit ?\nCombien de blocks (choisi-e le nombre) ?\nQuel mode (choisi-e parmi : Manuel ou Auto) ?\n\nForce & Honneur"""
        self.text_intro.insert(tk.END, self.text_itself)

        # Spinbox Button for Shifts
        self.shiftlabel = tk.Label(self.master, text="Shift", justify='left', font=18)
        self.shiftlabel.grid(row=2, column=3)
        self.shiftbutton = ttk.Spinbox(self.master, text="Shift", bootstyle="success", values= ["Morning", "Afternoon", "Night"], font=("Helvetica", 14)).grid(row=2, column=4, pady=10)

        # Spinbox Button for Blocks
        self.blockslabel = tk.Label(self.master, text="Selection de Blocks", justify='left', font=18)
        self.blockslabel.grid(row=4, column=3)
        self.blocksbutton = ttk.Spinbox(self.master, text="Blocks", bootstyle="success", from_=1, to=6, font=("Helvetica", 14)).grid(row=4, column=4, pady=10)

        # Checkbox Buttons Manuel vs Automation
        self.modelabel = tk.Label(self.master, text="Mode", justify='left', font=18)
        self.modelabel.grid(row=6, column=3)
        self.manualbutton = ttk.Checkbutton(self.master, text="Manual", bootstyle="success-round-toggle").grid(row=6, column=4, pady=10)
        self.autopilotbutton = ttk.Checkbutton(self.master, text="AutoPilot", bootstyle="success-round-toggle").grid(row=6, column=5, pady=10)
        self.prombutton = ttk.Checkbutton(self.master, text="Prom. Only", bootstyle="warning-round-toggle").grid(row=7, column=4, pady=10)
        self.prodbutton = ttk.Checkbutton(self.master, text="Prod. Only", bootstyle="warning-round-toggle").grid(row=7, column=5, pady=10)
        self.tradeoffbutton = ttk.Checkbutton(self.master, text="TradeOff P&P", bootstyle="warning-round-toggle").grid(row=7, column=8, pady=10)

        # Navigation Button
        self.navbutton = ttk.Button(self.master, text="Gestion Activite", bootstyle="PRIMARY", command= lambda: self.selecttab(1)).grid(row=12, column=4, pady=10)