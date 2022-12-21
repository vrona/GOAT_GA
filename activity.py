import tkinter as tk
import tkinter.messagebox
from tkinter import ttk
import adminblocks
from engine import Computing
import globaldb
from globaldb import UsingDB
from gauge import Meter
from ttkbootstrap.constants import *
import datetime

class Activity():
    def __init__(self, master):

        self.master = master
        self.rowpart = 4
        self.dictart_int = {}
        self.dictean_int = {}
        self.artgoal_input = {}
        self.eangoal_input = {}
        self.get_dictglobalpick = {}
        self.speedtheo_input = {}
        
        self.dictblockpickerout = {}

    def task_widget(self, lsofblock):
        
        self.lsofblock = lsofblock

        self.totalpicker_text = tk.IntVar()

        # BLOCKS PART
        self._block = tk.Label(self.master, text='BLOCKS', justify='center', font=('bold', 20), pady=10)
        self._block.grid(row=0, column=4, )

        self._article = tk.Label(self.master, text='Articles\nInitiaux', justify='right',font=("bold", 13), pady=10)
        self._article.grid(row=2, column=1)

        self.ean = tk.Label(self.master, text='EAN\nInitiaux', justify='right',font=("bold", 13), pady=10)
        self.ean.grid(row=3, column=1)

        self.articlegoal = tk.Label(self.master, text='Articles Goal', justify='right',font=("bold", 13), pady=10)
        self.articlegoal.grid(row= self.rowpart+13, column=1)

        self.eangoal = tk.Label(self.master, text='EAN Goal', justify='right',font=("bold", 13), pady=10)
        self.eangoal.grid(row=self.rowpart+14, column=1)

        self.speedtheo = tk.Label(self.master, text='Vitesse Theorique', justify='right',font=("bold", 13), pady=10)
        self.speedtheo.grid(row=self.rowpart+3, column=1)

        self.speedgoal = tk.Label(self.master, text='Vitesse Goal', justify='right',font=("bold", 13), pady=10)
        self.speedgoal.grid(row=self.rowpart+5, column=1)

        

        # POLY PART
        #self.poly_widget()


        # SEPARATOR & PICKERS PARTS
        #self.sep_pickers_widget()

        # TOTALS PART
        self.totrow = 21
        self._totals = tk.Label(self.master, text='TOTALS', justify='center', font=('bold', 16), pady=10)
        self._totals.grid(row=self.totrow, column=4)

        self.totalprelev = tk.Label(self.master, text='Total \nPrelev', font=("bold", 13), pady=10)
        self.totalprelev.grid(row=self.totrow+1, column=3)

        self.deltacap = tk.Label(self.master, text='Delta \nVitesse', font=("bold", 13), pady=10)
        self.deltacap.grid(row=self.totrow+1, column=4)

        self.totalpredprlv = tk.Label(self.master, text='Total \nPredic Prelev', font=("bold", 13), pady=10)
        self.totalpredprlv.grid(row=self.totrow+1, column=5)

        self.autoblock(self.lsofblock)

        self.totalpart()

        # Navigation Button
        self.navbutton = ttk.Button(self.master, text="Reporting", bootstyle="PRIMARY", command= lambda: self.selecttab(2)).grid(row=26, column=12, pady=10)

    def poly_widget(self):
        
        self._poly = tk.Label(self.master, text='POLY', justify='center', font=('bold', 20), pady=10)
        self._poly.grid(row=self.rowpart+4, column=4)

        self._currentopick = tk.Label(self.master, text='TP \nPresent', justify='center', font=('bold', 16), pady=10)
        self._currentopick.grid(row=self.rowpart+5, column=2)

        self.currentopick = tk.Listbox(self.master, height=5, width=10, justify="center")
        self.currentopick.grid(row=self.rowpart+6, column=2)

        self._theorytopick = tk.Label(self.master, text='TP \nTheorique', justify='center', font=('bold', 16), pady=10)
        self._theorytopick.grid(row=self.rowpart+5, column=4)

        self.theorytopick = tk.Listbox(self.master, height=5, width=10, justify="center")
        self.theorytopick.grid(row=self.rowpart+6, column=4)

        self._polystatus = tk.Label(self.master, text='Poly \nStatus', justify='center', font=('bold', 16), pady=10)
        self._polystatus.grid(row=self.rowpart+5, column=6)

        self.polystatus = tk.Listbox(self.master, height=5, width=10, justify="center")
        Meter(master=self.master, metersize=110, padding=20, amountused=-2, labeltext="Poly",
                meterstyle='warning.TLabel', metertype='semi', textfont=20).grid(row=self.rowpart+6, column=6)

    def sep_pickers_widget(self):
        # SEPARATOR PART
        self.seppoly1 = ttk.Separator(self.master, bootstyle="info")
        self.seppoly2 = ttk.Separator(self.master, bootstyle="info")
        self.seppoly1.grid(row=self.rowpart+4, column=1, sticky="nsew", rowspan=2, columnspan=1)
        self.seppoly2.grid(row=self.rowpart+4, column=5, sticky="nsew", rowspan=2, columnspan=3)
        
        # PICKERS PART
        self.picker_row = 10 # to merge
        self.hours = tk.Label(self.master, text='HEURE', font=("bold", 20), pady=10)
        self.hours.grid(row=self.picker_row, column=1)

        self.pickertitle = tk.Label(self.master, text='PICKERS', font=("bold", 20), pady=10)
        self.pickertitle.grid(row=self.picker_row, column=4)

    def input_art_ean(self):

        self.dkey = globaldb.lsartean
        limit = len(self.dkey) //2 -1 # getting the frontier between art and ean      

        self.get_dictart = dict(zip(self.dkey[1 : limit+1], self.dictart_int.values()))
        self.get_dictart = dict((key, value.get()) for key, value in self.get_dictart.items())
        self.get_dictean = dict(zip(self.dkey[limit+1 : len(self.dkey)-1], self.dictean_int.values()))
        self.get_dictean = dict((key, value.get()) for key, value in self.get_dictean.items())
        self.timerecord = datetime.datetime.now()

        self.get_dictglobalpick = {'time_glob': self.timerecord, **self.get_dictart,**self.get_dictean, 'total_pickers':self.totalpicker_text.get()}
        
        for key in self.get_dictglobalpick.keys():
            if self.get_dictglobalpick[key] == 0: 
                tkinter.messagebox.showerror(
                    "Champs requis", "Remplissez les champs, svp")
                return

        # Insert into DB
        pdb = UsingDB("./database/goatdata.db")
        engindb = Computing("./database/goatdata.db")
        pdb.insert_dicsql(self.get_dictglobalpick, "in_globalpick")

        engindb.weightnratio(self.get_dictglobalpick)
        engindb.new_goal()
        engindb.speedness()

        # Displaying the goals
        for ba, rowa, rowe in zip(range(0, len(globaldb.ls_goal_g)//2), pdb.fetch_artgoal(), pdb.fetch_eangoal()):
            self.artgoal_input[ba].insert(tk.END, rowa)
            self.eangoal_input[ba].insert(tk.END, rowe)

        # Displaying the speedtheo
        for k, val in adminblocks.speedtheodict.items():
            self.speedtheo_input[adminblocks.mainlistblock.index(k)].insert(tk.END, val)

    def autoblock(self, lsofblock):

        self.part_art_input = {}
        self.part_ean_input = {}
        
        self.speed_input = {}
        self.lsofblock = lsofblock
        
        for nblock in self.lsofblock:

            self.dictart_int[self.lsofblock.index(nblock)] = tk.IntVar()
            self.dictean_int[self.lsofblock.index(nblock)] = tk.IntVar()

            self.speed_input[self.lsofblock.index(nblock)] = tk.IntVar()
            
            self.part_block = tk.Label(self.master, text=self.lsofblock[self.lsofblock.index(nblock)], font=("bold", 12))
            self.part_block.grid(row=1, column=self.lsofblock.index(nblock)+2)

            self.part_art_input[self.lsofblock.index(nblock)] = tk.Entry(self.master, textvariable=self.dictart_int[self.lsofblock.index(nblock)], justify="center", width=10)
            self.part_art_input[self.lsofblock.index(nblock)].grid(row=2, column=self.lsofblock.index(nblock)+2)

            self.part_ean_input[self.lsofblock.index(nblock)] = tk.Entry(self.master, textvariable=self.dictean_int[self.lsofblock.index(nblock)], justify="center", width=10)
            self.part_ean_input[self.lsofblock.index(nblock)].grid(row=3, column=self.lsofblock.index(nblock)+2)

            self.artgoal_input[self.lsofblock.index(nblock)] = tk.Listbox(self.master, justify="center", height=1, width=10)#, textvariable=self.dictart_goal[self.lsofblock.index(nblock)], state=tk.DISABLED)
            self.artgoal_input[self.lsofblock.index(nblock)].grid(row= self.rowpart+13, column=self.lsofblock.index(nblock)+2)

            self.eangoal_input[self.lsofblock.index(nblock)] = tk.Listbox(self.master, justify="center", height=1, width=10) #, textvariable=self.dictean_goal[self.lsofblock.index(nblock)]state=tk.DISABLED)
            self.eangoal_input[self.lsofblock.index(nblock)].grid(row= self.rowpart+14, column=self.lsofblock.index(nblock)+2)

            self.speedtheo_input[self.lsofblock.index(nblock)] = tk.Listbox(self.master, justify="center", height=1, width=10)
            self.speedtheo_input[self.lsofblock.index(nblock)].grid(row=self.rowpart+3, column=self.lsofblock.index(nblock)+2)

            self.speedgoal_input = tk.Listbox(self.master, justify="center", height=1, width=10) # textvariable=adminblocks.speedtheodict[nblock]
            self.speedgoal_input.grid(row=self.rowpart+5, column=self.lsofblock.index(nblock)+2)

            Meter(master=self.master, metersize=130, padding=20, stripethickness=2, amountused=10, labeltext=self.lsofblock[self.lsofblock.index(nblock)], textappend='%',
                 meterstyle='success.TLabel').grid(row=22, column=self.lsofblock.index(nblock)+2)
            
            self.totalpicker = tk.Label(self.master, text='Total Pickers', font=("bold", 13), pady=10)
            self.totalpicker.grid(row=1, column=self.lsofblock.index(self.lsofblock[-1])+4)

            self.totalpicker_input = tk.Entry(self.master, textvariable=self.totalpicker_text, justify="center", width=10)
            self.totalpicker_input.grid(row=2, column=self.lsofblock.index(self.lsofblock[-1])+4)

            self.buttondata = ttk.Button(self.master, text="GOAT Power", bootstyle="success", command=self.input_art_ean)
            self.buttondata.grid(row=3, column=self.lsofblock.index(self.lsofblock[-1])+5 , padx=10)

    def totalpart(self):

        self.totalprelev_list = tk.Listbox(self.master, height=1, width=10, justify="center")
        self.totalprelev_list.grid(row=25, column=3)

        self.deltacap_list = tk.Listbox(self.master, height=1, width=10, justify="center")
        self.deltacap_list.grid(row=25, column=4)
        
        self.totalpredprlv_list = tk.Listbox(self.master, height=1, width=10, justify="center")
        self.totalpredprlv_list.grid(row=25, column=5)
