import tkinter as tk
import tkinter.messagebox
# from tkinter import ttk
import ttkbootstrap as ttk
import adminblocks
from engine import Computing
from dispatch import Dispatch
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
        self.speedinitial_input = {}
        self.dictblockpickerout = {}
        self.picker_name = {}

    def task_widget(self, lsofblock):
        
        self.lsofblock = lsofblock

        self.totalpicker_text = tk.IntVar()

        # BLOCKS PART
        self._block = tk.Label(self.master, text='BLOCKS', justify='center', font=('bold', 20), pady=10)
        self._block.grid(row=0, column= len(adminblocks.mainlistblock)//2 +2)

        self._article = tk.Label(self.master, text='Articles\nTablette', justify='center',font=("bold", 13), pady=10)
        self._article.grid(row=2, column=1)

        self.ean = tk.Label(self.master, text='EAN\nTablette', justify='center',font=("bold", 13), pady=10)
        self.ean.grid(row=3, column=1)

        self.speedtheo = tk.Label(self.master, text='Vitesse Initiale \nart./picker/h.', justify='center',font=("bold", 13), pady=10)
        self.speedtheo.grid(row=self.rowpart, column=1)
        
        self.articlegoal = tk.Label(self.master, text='Articles Goal', justify='center',font=("bold", 13), pady=10)
        self.articlegoal.grid(row= self.rowpart+1, column=1)

        self.eangoal = tk.Label(self.master, text='EAN Goal', justify='center',font=("bold", 13), pady=10)
        self.eangoal.grid(row=self.rowpart+2, column=1)

        self.speedgoal = tk.Label(self.master, text='Vitesse Goal Block\nart./h.', justify='center',font=("bold", 13), pady=10)
        self.speedgoal.grid(row=self.rowpart+3, column=1)

        self.speedrealt = tk.Label(self.master, text='Vitesse réelle\nart./picker/h.', justify='center',font=("bold", 13), pady=10)
        self.speedrealt.grid(row=self.rowpart+4, column=1)

        # SEPARATOR & PICKERS PARTS
        self.sep_pickers_widget()

        self.autoblock(self.lsofblock)
        self.pickrhour()
        self.totalpart()

    def sep_widget(self, location):
        # SEPARATOR PART
        self.seppoly1 = ttk.Separator(self.master, bootstyle="info")
        self.seppoly2 = ttk.Separator(self.master, bootstyle="info")
        self.seppoly1.grid(row=self.rowpart+location, column=1, sticky="nsew", columnspan= len(adminblocks.mainlistblock)//2 +1)
        self.seppoly2.grid(row=self.rowpart+location, column=len(adminblocks.mainlistblock)//2 +1, sticky="nsew", columnspan= len(adminblocks.mainlistblock)//2 +3)

    def sep_pickers_widget(self):
        # SEPARATOR PART
        self.sep_widget(7)
        
        # PICKERS PART
    
    def pickrhour(self):

        self.pickertitle = tk.Label(self.master, text='PICKERS', font=("bold", 20), pady=10)
        self.pickertitle.grid(row=self.rowpart+7, column=len(adminblocks.mainlistblock)//2 +2)

        self.hours = tk.Label(self.master, text='HEURE', font=("bold", 12), pady=10)
        self.hours.grid(row=self.rowpart+8, column=1)
     
        self.hourofdispatch = tk.Listbox(self.master, height=1, width=25, justify="center", font=14)
        self.hourofdispatch.grid(row=self.rowpart+9, column=1)
        
        for nblock in adminblocks.mainlistblock:

            self.dictblockpickerout[adminblocks.mainlistblock.index(nblock)] = tk.Listbox(self.master, height=1, width=5, justify="center")
            self.dictblockpickerout[adminblocks.mainlistblock.index(nblock)].grid(row=self.rowpart+9, column=adminblocks.mainlistblock.index(nblock)+2)
            self.picker_name[adminblocks.mainlistblock.index(nblock)] = tk.Listbox(self.master, height=8, width=10, justify="center")
            self.picker_name[adminblocks.mainlistblock.index(nblock)].grid(row=self.rowpart+11, column=adminblocks.mainlistblock.index(nblock)+2)

    # TOTALS PART 
    def totalpart(self):
         
        self.totrow = 21


    def input_art_ean(self):
        self.clear_listbox()
        self.dkey = globaldb.lsartean
        limit = len(self.dkey) //2 -1 # getting the frontier between art and ean      

        self.get_dictart = dict(zip(self.dkey[1 : limit+1], self.dictart_int.values()))
        self.get_dictart = dict((key, value.get()) for key, value in self.get_dictart.items())
        self.get_dictean = dict(zip(self.dkey[limit+1 : len(self.dkey)-1], self.dictean_int.values()))
        self.get_dictean = dict((key, value.get()) for key, value in self.get_dictean.items())
        self.timerecord = datetime.datetime.now()

        self.get_dictglobalpick = {'time_glob': self.timerecord, **self.get_dictart,**self.get_dictean, 'total_pickers':self.totalpicker_text.get()}
        
        # for key in self.get_dictglobalpick.keys():
        #     if self.get_dictglobalpick[key] == 0: 
        #         tkinter.messagebox.showerror(
        #             "Champs requis", "Remplissez les champs, svp")
        #         return

        # Insert into DB
        pdb = UsingDB()
        enginedb = Computing()
        dispatch = Dispatch()

        pdb.insert_dicsql(self.get_dictglobalpick, "in_globalpick")
        enginedb.weightnratio(self.get_dictglobalpick)
        
        #insert new picker
        enginedb.insert_new_picker(self.totalpicker_text.get())

        # setting goals
        enginedb.new_goal()
        
        # computes speedness of blocks
        self.speedpkr = enginedb.speedness()

        # retrieve pickers and poly needs
        self.dispatch_pkr, self.tot_opti_pkr, self.poly_value = dispatch.pkrandpoly()

        # Displaying the goals
        for ba, rowa, rowe in zip(range(0, len(globaldb.ls_goal_g)//2), pdb.fetch_artgoal(), pdb.fetch_eangoal()):
            self.artgoal_input[ba].insert(tk.END, rowa)
            self.eangoal_input[ba].insert(tk.END, rowe)

        # Displaying the initial_speed
        for k, val in adminblocks.speedtheodict.items():
            self.speedinitial_input[adminblocks.mainlistblock.index(k)].insert(tk.END, val)

        # Displaying TP Present
        #self.currentopick.insert(tk.END, self.get_dictglobalpick['total_pickers'])

        # Displaying TP Necessaire
        self.neededpickr.insert(tk.END, self.tot_opti_pkr)
        
        # Displaying Poly num
        self.polystatus.insert(tk.END, self.poly_value)
        if self.poly_value < 0:
            self.polystatus.itemconfig(0, {'bg' : '#ED2939'})
        else:
            self.polystatus.itemconfig(0, {'bg' : '#00A86B'})
        
        # Displaying hour and pickers per block
        self.hourofdispatch.insert(tk.END, self.get_dictglobalpick['time_glob'])
        for keys, vals in self.dispatch_pkr.items():
            self.dictblockpickerout[adminblocks.mainlistblock.index(keys)].insert(tk.END, vals)
        
        for speed in range(len(adminblocks.mainlistblock)):
            self.speed_goal[speed].insert(tk.END,  self.speedpkr['speed_goal_artbck{}'.format(speed)])
            self.speed_realtime[speed].insert(tk.END,  self.speedpkr['speed_artbck{}'.format(speed)])
    
        # Displaying pickers dispatch
        dispatch.dispatchme(datetime.datetime.now())
       
        # Displaying gauges and total
        if enginedb.totalongoal() is not None:
            self.percent_picked, self.totalofit = enginedb.totalongoal()
            # Gauge
            for ncolit in range(len(adminblocks.mainlistblock)):
                Meter(master=self.master, metersize=98, padding=15, stripethickness=2, amountused=self.percent_picked[ncolit], labeltext=adminblocks.mainlistblock[ncolit], textappend='%', textfont= 'Helvetica 12 bold',
                meterstyle='success.TLabel').grid(row=self.rowpart+16, column=ncolit+2)
            self.totalofit = self.totalofit

            self.totalpicked.insert(tk.END, self.totalofit[0])

    def autoblock(self, lsofblock):

        self.part_art_input = {}
        self.part_ean_input = {}
        self.speed_goal = {}
        self.speed_realtime = {}
        self.lsofblock = lsofblock      
        
        for nblock in self.lsofblock:

            self.dictart_int[self.lsofblock.index(nblock)] = tk.IntVar()
            self.dictean_int[self.lsofblock.index(nblock)] = tk.IntVar()
            
            self.part_block = tk.Label(self.master, text=self.lsofblock[self.lsofblock.index(nblock)], font=("bold", 12))
            self.part_block.grid(row=1, column=self.lsofblock.index(nblock)+2)

            self.part_art_input[self.lsofblock.index(nblock)] = tk.Entry(self.master, textvariable=self.dictart_int[self.lsofblock.index(nblock)], justify="center", width=10)
            self.part_art_input[self.lsofblock.index(nblock)].grid(row=2, column=self.lsofblock.index(nblock)+2)

            self.part_ean_input[self.lsofblock.index(nblock)] = tk.Entry(self.master, textvariable=self.dictean_int[self.lsofblock.index(nblock)], justify="center", width=10)
            self.part_ean_input[self.lsofblock.index(nblock)].grid(row=3, column=self.lsofblock.index(nblock)+2)

            self.speedinitial_input[self.lsofblock.index(nblock)] = tk.Listbox(self.master, justify="center", height=1, width=10)
            self.speedinitial_input[self.lsofblock.index(nblock)].grid(row=self.rowpart, column=self.lsofblock.index(nblock)+2)

            self.artgoal_input[self.lsofblock.index(nblock)] = tk.Listbox(self.master, justify="center", height=1, width=10)
            self.artgoal_input[self.lsofblock.index(nblock)].grid(row= self.rowpart+1, column=self.lsofblock.index(nblock)+2, padx=15)

            self.eangoal_input[self.lsofblock.index(nblock)] = tk.Listbox(self.master, justify="center", height=1, width=10)
            self.eangoal_input[self.lsofblock.index(nblock)].grid(row= self.rowpart+2, column=self.lsofblock.index(nblock)+2)

            self.speed_goal[self.lsofblock.index(nblock)] = tk.Listbox(self.master, justify="center", height=1, width=10)
            self.speed_goal[self.lsofblock.index(nblock)].grid(row=self.rowpart+3, column=self.lsofblock.index(nblock)+2)

            self.speed_realtime[self.lsofblock.index(nblock)] = tk.Listbox(self.master, justify="center", height=1, width=10)
            self.speed_realtime[self.lsofblock.index(nblock)].grid(row=self.rowpart+4, column=self.lsofblock.index(nblock)+2)
            
            self.totalpicker = tk.Label(self.master, text='Pickers \nPresents', font=("bold", 13), pady=10)
            self.totalpicker.grid(row=1, column=self.lsofblock.index(self.lsofblock[-1])+4)

            self.totalpicker_input = tk.Entry(self.master, textvariable=self.totalpicker_text, justify="center", width=10)
            self.totalpicker_input.grid(row=2, column=self.lsofblock.index(self.lsofblock[-1])+4)

            # self._currentopick = tk.Label(self.master, text='Total Pickers \nprésents', justify='center', font=('bold', 16), pady=10)
            # self._currentopick.grid(row=self.rowpart+5, column=2)

            # self.currentopick = tk.Listbox(self.master, height=1, width=8, justify="center", font=('bold', 15))
            # self.currentopick.grid(row=self.rowpart+6, column=2)

            self._neededpickr = tk.Label(self.master, text='Pickers \nnécessaires', justify='center', font=('bold', 13), pady=10)
            self._neededpickr.grid(row=3, column=self.lsofblock.index(self.lsofblock[-1])+4)

            self.neededpickr = tk.Listbox(self.master, height=1, width=8, justify="center", font=('bold', 14))
            self.neededpickr.grid(row=4, column=self.lsofblock.index(self.lsofblock[-1])+4)

            self._polystatus = tk.Label(self.master, text='Poly \nStatus', justify='center', font=('bold', 13), pady=10)
            self._polystatus.grid(row=5, column=self.lsofblock.index(self.lsofblock[-1])+4)

            self.polystatus = tk.Listbox(self.master, height=1, width=8, justify="center", font=('bold', 14))
            self.polystatus.grid(row=6, column=self.lsofblock.index(self.lsofblock[-1])+4)

            self.buttondata = ttk.Button(self.master, text="GOAT Power", bootstyle="success", command=self.input_art_ean)
            self.buttondata.grid(row=2, column=self.lsofblock.index(self.lsofblock[-1])+6 , padx=10)

            self._totals = tk.Label(self.master, text='TOTALS', justify='center', font=('bold', 16), pady=10)
            self._totals.grid(row=self.rowpart+7, column=self.lsofblock.index(self.lsofblock[-1])+4)

            self.totalpickedn = tk.Label(self.master, text='Total \nPicked', font=("bold", 13), pady=10)
            self.totalpickedn.grid(row=self.rowpart+15, column=self.lsofblock.index(self.lsofblock[-1])+4)

            self.totalpredpick = tk.Label(self.master, text='Total \nPrediction', font=("bold", 13), pady=10)
            self.totalpredpick.grid(row=self.rowpart+15, column=self.lsofblock.index(self.lsofblock[-1])+6)

            self.totalpicked = tk.Listbox(self.master, height=1, width=10, justify="center")
            self.totalpicked.grid(row=self.rowpart+16, column=self.lsofblock.index(self.lsofblock[-1])+4)
            
            self.totalpredpick_list = tk.Listbox(self.master, height=1, width=10, justify="center")
            self.totalpredpick_list.grid(row=self.rowpart+16, column=self.lsofblock.index(self.lsofblock[-1])+6)

            # Navigation Button
            self.navbutton = ttk.Button(self.master, text="Reporting", bootstyle="PRIMARY", command= lambda: self.selecttab(2))
            self.navbutton.grid(row=23, column=self.lsofblock.index(self.lsofblock[-1])+6, pady=10)
              

    # Clear all listbox
    def clear_listbox(self):
        # self.currentopick.delete(0, tk.END)
        self.neededpickr.delete(0, tk.END)
        self.polystatus.delete(0, tk.END)
        self.hourofdispatch.delete(0, tk.END)
        self.totalpicked.delete(0, tk.END)
        for k in self.dictblockpickerout.keys():
            self.dictblockpickerout[k].delete(0, tk.END)
            self.speed_goal[k].delete(0, tk.END)
            self.speed_realtime[k].delete(0, tk.END)