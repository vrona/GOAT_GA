import tkinter as tk
import tkinter.messagebox
from tkinter import ttk
from globaldb import ProdDB
from PIL import Image, ImageTk
from gauge import Meter
from ttkbootstrap import Style
#from tkinter.ttk import Style
from ttkbootstrap.constants import *
import datetime
from globaldb import ProdDB
from adminblocks import Blocks
import adminblocks
import globaldb

dictart_int = {}
dictean_int = {}

class PickGAApp(tk.Frame):
    
    def __init__(self, master):
        super().__init__(master)
        self.get_dictglobalpick = {}
        
        self.dictblockpickerout = {}
        self.root = master
        #self.root = tk.Tk()
        self.root.title("GOAT Of GA (alpha)")
        self.root.geometry("1600x1080")
        self.tabcontrol = ttk.Notebook(self.root)
        self.tabcontrol.grid(pady=5)

        #self.config = tk.Frame(self.tabcontrol, width= 1600, height=1080)
        self.activity = tk.Frame(self.tabcontrol, width= 1600, height=1080)
        self.reporting = tk.Frame(self.tabcontrol, width= 1600, height=1080)
        self.admin = tk.Frame(self.tabcontrol, width= 1600, height=1080)
        self.credit = tk.Frame(self.tabcontrol, width= 1600, height=1080)

        #self.config.pack(fill="both", expand=1)
        self.activity.pack(fill="both", expand=1)
        self.reporting.pack(fill="both", expand=1)
        self.admin.pack(fill="both", expand=1)
        self.credit.pack(fill="both", expand=1)


        #self.tabcontrol.add(self.config, text="Blocks Configuration")
        self.tabcontrol.add(self.admin, text="AdminOnly")
        self.tabcontrol.add(self.activity, text="Task Management")
        self.tabcontrol.add(self.reporting, text="Reporting")
        self.tabcontrol.add(self.credit, text="Credits")

        # Admin widget's Validation & Launch Buttons
        self.validblock_btn = ttk.Button(self.admin, text="Valider Blocks", bootstyle="danger", command=lambda:[Blocks(self.admin).validate_block(), self.ready(), self.switchstate()], width=12)
        self.validblock_btn.grid(row=17, column=1, pady=10)

        self.launch_btn = ttk.Button(self.admin, text="Lancer Activité", style='valid.btn', width=12, command=lambda:self.selecttab(1), state=tk.DISABLED) #, 
        self.launch_btn.grid(row=20, column=1)

        Blocks(self.admin)

        #Configtab(self.config).configwidget(self.selecttab)
        self.credit_widget()
    
    def switchstate(self):
        self.launch_btn["state"]=tk.NORMAL
        self.validblock_btn["state"]=tk.DISABLED

    def ready(self):
        # self.listofcell = Blocks(self.admin).lisfofblock()
        # self.task_widget(self.listofcell)
        self.task_widget(adminblocks.mainlistblock)

    def selecttab(self, tab):
        self.tab = tab
        self.tabcontrol.select(self.tab)
    
    def credit_widget(self):
        self.imagecestas = Image.open("./logo/LogoCestasDC2024.png")
        self.vronalogo = Image.open("./logo/vrona_sas_logo_corporate.png")

        self.resized_cestas= self.imagecestas.resize((242,200))
        self.resized_vrona= self.vronalogo.resize((140,140))

        self.rcestasimg = ImageTk.PhotoImage(self.resized_cestas)
        self.rvronaimg = ImageTk.PhotoImage(self.resized_vrona)

        self.cestasimg_credit = tk.Label(self.credit, image=self.rcestasimg)
        self.vronaimg_credit = tk.Label(self.credit, image=self.rvronaimg)

        self.cestasimg_credit.image = self.rcestasimg
        self.vronaimg_credit.image = self.rvronaimg

        self.cestasimg_credit.place(x=700, y=240)
        self.vronaimg_credit.place(x=750, y=558)

        self.credit_text = tk.Label(self.credit, text = "App: GOAT_GA\nTasks Recommendation System\nversion: alpha v1.00\nAuthor: Michael Hatchi")
        self.credit_text.place(x=726, y=460)

        self.rights_text = tk.Label(self.credit, text = "Copyright © VRONA SAS\nAll rights reserved. \nLicense: XXX")
        self.rights_text.place(x=750, y=690)

    def task_widget(self, lsofblock):
        
        self.lsofblock = lsofblock

        self.totalpicker_text = tk.IntVar()

        # BLOCKS PART
        self._block = tk.Label(self.activity, text='BLOCKS', justify='center', font=('bold', 20), pady=10)
        self._block.grid(row=0, column=4, )

        self._article = tk.Label(self.activity, text='Articles', justify='right',font=("bold", 13), pady=10)
        self._article.grid(row=2, column=1)

        self.ean = tk.Label(self.activity, text='EAN', justify='right',font=("bold", 13), pady=10)
        self.ean.grid(row=3, column=1)

        self.totalpicker_input = tk.Entry(self.activity, textvariable=self.totalpicker_text, justify="center", width=10)
        self.totalpicker_input.grid(row=2, column=9)

        self.buttondata = ttk.Button(self.activity, text="GOAT Power", bootstyle="success", command=self.add_arteanpik)
        self.buttondata.grid(row=3, column=12 , padx=10)

        # POLY PART
        self._poly = tk.Label(self.activity, text='POLY', justify='center', font=('bold', 20), pady=10)
        self._poly.grid(row=5, column=4)

        self._currentopick = tk.Label(self.activity, text='TP \nPresent', justify='center', font=('bold', 16), pady=10)
        self._currentopick.grid(row=6, column=2)

        self.currentopick = tk.Listbox(self.activity, height=5, width=10, justify="center")
        self.currentopick.grid(row=7, column=2)

        self._theorytopick = tk.Label(self.activity, text='TP \nTheorique', justify='center', font=('bold', 16), pady=10)
        self._theorytopick.grid(row=6, column=4)

        self.theorytopick = tk.Listbox(self.activity, height=5, width=10, justify="center")
        self.theorytopick.grid(row=7, column=4)

        self._polystatus = tk.Label(self.activity, text='Poly \nStatus', justify='center', font=('bold', 16), pady=10)
        self._polystatus.grid(row=6, column=6)

        self.polystatus = tk.Listbox(self.activity, height=5, width=10, justify="center")
        Meter(master=self.activity, metersize=110, padding=20, amountused=-2, labeltext="Poly",
                meterstyle='warning.TLabel', metertype='semi', textfont=20).grid(row=7, column=6)

        # SEPARATOR PART
        
        # self.separator = ttk.Separator(bootstyle="info")
        # self.separator.grid(row=4, column=1, sticky="nsew", rowspan=2, columnspan=9)
        
        # PICKERS PART
        self.picker_row = 10 # to merge
        self.hours = tk.Label(self.activity, text='HEURE', font=("bold", 20), pady=10)
        self.hours.grid(row=self.picker_row, column=1)

        self.pickertitle = tk.Label(self.activity, text='PICKERS', font=("bold", 20), pady=10)
        self.pickertitle.grid(row=self.picker_row, column=4)

        # TOTALS PART
        self._totals = tk.Label(self.activity, text='TOTALS', justify='center', font=('bold', 16), pady=10)
        self._totals.grid(row=23, column=4)

        self.totalprelev = tk.Label(self.activity, text='Total \nPrelev', font=("bold", 13), pady=10)
        self.totalprelev.grid(row=24, column=3)

        self.deltacap = tk.Label(self.activity, text='Delta \nCapacitif', font=("bold", 13), pady=10)
        self.deltacap.grid(row=24, column=4)

        self.totalpredprlv = tk.Label(self.activity, text='Total \nPredic Prelev', font=("bold", 13), pady=10)
        self.totalpredprlv.grid(row=24, column=5)

        self.autoblock(self.lsofblock)

        self.totalpart()

        # Navigation Button
        self.navbutton = ttk.Button(self.activity, text="Reporting", bootstyle="PRIMARY", command= lambda: self.selecttab(2)).grid(row=26, column=12, pady=10)

    def autohour(self):
        
        # mise à jour automatique après validation Bouton des chiffres: outout -> hourout, dictblockpickerout, totalpickerout
        #self.lines = [5,7,9,11,13,15,17,19]

        self.hour_row = 9 # to merge
        self.hourname = tk.Label(self.activity, text="H", font=("bold", 13), padx=40, pady=10)
        self.hourout = tk.Listbox(self.activity, height=1, width=25, justify="center")
        self.totalpickerout = tk.Listbox(self.activity, height=1, width=5, justify="center")
        self.hourname.grid(row=self.hour_row, column=0)
        self.hourout.grid(row=self.hour_row, column=1)
        
        for nblock in self.listofcell:
            
            self.dictblockpickerout[self.listofcell.index(nblock)+1] = tk.Listbox(self.activity, height=1, width=5, justify="center")
            self.dictblockpickerout[self.listofcell.index(nblock)+1].grid(row=self.hour_row, column=self.listofcell.index(nblock)+2)
            
            self.totalpickerout.grid(row=self.hour_row, column=self.listofcell.index(self.listofcell[-1])+4)

    def get_timepickeroutput(self, block_num):
        pdb = ProdDB(block_num, "/Volumes/vrona_SSD/GOAT_GA/database/goatdata.db")
        self.theorytopick.delete(0, tk.END)
        self.autohour()
        for self.block_id in range(1, block_num +1):
        
        
        #self.dictblockpickerout[self.block_id].delete(0, tk.END)
        #self.totalpickerout.delete(0, tk.END)
        # fetch hour
            for row in pdb.fetch_hourout():
                self.hourout.insert(tk.END, row)
            # fetch picker
            for row in pdb.fetch_picker(self.block_id):
                self.dictblockpickerout[self.block_id].insert(tk.END, row)
            # fetch total
            for row in pdb.fetch_total_picker():
                self.totalpickerout.insert(tk.END, row)
                self.theorytopick.insert(tk.END, row)

    def add_arteanpik(self):
        # DEAD DEAD DEAD DEAD DEAD DEAD DEAD DEAD
        
        self.dkey = globaldb.lsartean
        limit = len(self.dkey) //2 -1 # getting the frontier between art and ean      

        self.get_dictart = dict(zip(self.dkey[1 : limit+1], dictart_int.values()))
        self.get_dictart = dict((key, value.get()) for key, value in self.get_dictart.items())
        self.get_dictean = dict(zip(self.dkey[limit+1 : len(self.dkey)-1], dictean_int.values()))
        self.get_dictean = dict((key, value.get()) for key, value in self.get_dictean.items())
        self.timerecord = datetime.datetime.now()
        self.get_dictglobalpick = {'time_glob': self.timerecord, **self.get_dictart,**self.get_dictean, 'total_pickers':self.totalpicker_text.get()}
               
        # if (self.get_dictglobalpick[key] == '' for key in self.get_dictglobalpick.keys()):
        #     tkinter.messagebox.showerror(
        #         "Champs requis", "Remplissez les champs, svp")
        #     return
        #print(self.get_dictglobalpick[key] == '' for key in self.get_dictglobalpick.keys())

        # Insert into DB
        pdb = ProdDB(len(self.dkey)-2,"/Volumes/vrona_SSD/GOAT_GA/database/goatdata.db")
        pdb.insert_gpick(self.get_dictglobalpick)
        #pdb.insert_poly(self.timerecord, self.totalpicker_text.get(), , )
            
        # Insert into list
        #self.hourout.insert(self.get_dictglobalpick['time_glob'])

        #     self.dictblockpickerout[self.lsofblock.index(nblock)].insert(dictart_int[self.lsofblock.index(nblock)].get(), dictean_int[self.lsofblock.index(nblock)].get(),
        #             self.totalpicker_text.get())
            #self.clear_text(nblock)
        self.get_timepickeroutput(len(self.dkey)-2)

    def autoblock(self, lsofblock):

        self.part_art_input = {}
        self.lsofblock = lsofblock
        
        for nblock in self.lsofblock:
            dictart_int[self.lsofblock.index(nblock)] = tk.IntVar()
            dictean_int[self.lsofblock.index(nblock)] = tk.IntVar()
            

            self.part_block = tk.Label(self.activity, text=self.lsofblock[self.lsofblock.index(nblock)], font=("bold", 12))
            self.part_block.grid(row=1, column=self.lsofblock.index(nblock)+2)

            self.part_art_input[self.lsofblock.index(nblock)+1] = tk.Entry(self.activity, textvariable=dictart_int[self.lsofblock.index(nblock)], justify="center", width=10)
            self.part_art_input[self.lsofblock.index(nblock)+1].grid(row=2, column=self.lsofblock.index(nblock)+2)

            self.part_ean_input = tk.Entry(self.activity, textvariable=dictean_int[self.lsofblock.index(nblock)], justify="center", width=10)
            self.part_ean_input.grid(row=3, column=self.lsofblock.index(nblock)+2)

            Meter(master=self.activity, metersize=130, padding=20, stripethickness=2, amountused=10, labeltext=self.lsofblock[self.lsofblock.index(nblock)], textappend='%',
                 meterstyle='success.TLabel').grid(row=22, column=self.lsofblock.index(nblock)+2)
            
            self.totalpicker = tk.Label(self.activity, text='Total Pickers', font=("bold", 13), pady=10)
            self.totalpicker.grid(row=1, column=self.lsofblock.index(self.lsofblock[-1])+4)

    def totalpart(self):

        self.totalprelev_list = tk.Listbox(self.activity, height=2, width=10, justify="center")
        self.totalprelev_list.grid(row=25, column=3)

        self.deltacap_list = tk.Listbox(self.activity, height=2, width=10, justify="center")
        self.deltacap_list.grid(row=25, column=4)
        
        self.totalpredprlv_list = tk.Listbox(self.activity, height=2, width=10, justify="center")
        self.totalpredprlv_list.grid(row=25, column=5)

    def notready(self):
        # Text
        self.text_intro = tk.Text(self.activity, height=25, font=30,width= 40)
        self.text_intro.place(x=200,y=10)

        self.text_itself = """Pour lancer l'activité,\nles Blocks doivent être CONFIGURES et VALIDES"""
        self.text_intro.insert(tk.END, self.text_itself)


    # def clear_text(self, nblocks):
    #     self.nblocks = nblocks
    #     self.part_art_input[self.nblocks].delete(0, tk.END)
    #     self.part_ean_input.delete(0, tk.END)

    def mainloop(self):
    #     #style = Style('litera')
        
        self.root.mainloop()


root = tk.Tk()
style = Style('flatly')
style.master
app = PickGAApp(master = root) #, master=root listofcell=listofoutdoor

# root = style.master
# style.master.mainloop()
app.mainloop()