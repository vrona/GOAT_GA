from ast import Delete
import tkinter as tk
import tkinter.messagebox
from tkinter import ttk
from globaldb import ProdDB
from PIL import Image, ImageTk
from gauge import Meter
from ttkbootstrap import Style
from ttkbootstrap.constants import *
import datetime


listofoutdoor = ["SportCo", "Chasse", "Glisse", "Running", "Implant", "PFECA"]
pdb = ProdDB("./database/goatdata.db")

class PickGAApp(tk.Frame):

    def __init__(self, master, listofcell):
        super().__init__(master)
        self.get_dictglobalpick = {}
        self.dictart_int = {}
        self.dictean_int = {}
        self.dictblockpickerout = {} # dict picker/block
        #self.dict_hourname = {}
        #self.dict_hourout = {}
        self.master = master
        self.listofcell = listofcell
        self.iniblock(self.listofcell)
        master.title("GOAT Of GA (alpha)")
        master.geometry("1600x1080")
        #master.resizable(False, False)
        self.backgd()
        self.block_widget(self.listofcell)
        self.totalpart()
    
    def backgd(self):
        self.imagecestas = Image.open("./logo/LogoCestasDC2024.png")
        self.resized_image= self.imagecestas.resize((121,100))
        self.test = ImageTk.PhotoImage(self.resized_image)
        self.label1 = tkinter.Label(image=self.test)
        self.label1.image = self.test

        self.label1.place(x=15, y=35)

    def iniblock(self, listofblock):
        self.listofblock = listofblock
        for data in self.listofblock:
            
            pdb.insert_nameblock(self.listofblock.index(data)+1, "{}".format(data))
 
    def block_widget(self, lsofblock):
        self.lsofblock = lsofblock

        self.totalpicker_text = tk.IntVar()

        # BLOCKS PART
        self._block = tk.Label(self.master, text='BLOCKS', justify='center', font=('bold', 20), pady=10)
        self._block.grid(row=0, column=4, )

        self._article = tk.Label(self.master, text='Articles', justify='right',font=("bold", 13), pady=10)
        self._article.grid(row=2, column=1)

        self.ean = tk.Label(self.master, text='EAN', justify='right',font=("bold", 13), pady=10)
        self.ean.grid(row=3, column=1)

        self.totalpicker_input = tk.Entry(self.master, textvariable=self.totalpicker_text, justify="center", width=10)
        self.totalpicker_input.grid(row=2, column=9)

        self.buttondata = ttk.Button(root, text="GOAT Power", bootstyle=SUCCESS, command=self.add_ateanpik)
        self.buttondata.grid(row=3, column=12 , padx=10)

        # POLY PART
        self._poly = tk.Label(self.master, text='POLY', justify='center', font=('bold', 20), pady=10)
        self._poly.grid(row=5, column=4)

        self._currentopick = tk.Label(self.master, text='TP \nPresent', justify='center', font=('bold', 16), pady=10)
        self._currentopick.grid(row=6, column=2)

        self.currentopick = tk.Listbox(self.master, height=5, width=10, justify="center")
        self.currentopick.grid(row=7, column=2)

        self._theorytopick = tk.Label(self.master, text='TP \nTheorique', justify='center', font=('bold', 16), pady=10)
        self._theorytopick.grid(row=6, column=4)

        self.theorytopick = tk.Listbox(self.master, height=5, width=10, justify="center")
        self.theorytopick.grid(row=7, column=4)

        self._polystatus = tk.Label(self.master, text='Poly \nStatus', justify='center', font=('bold', 16), pady=10)
        self._polystatus.grid(row=6, column=6)

        self.polystatus = tk.Listbox(self.master, height=5, width=10, justify="center")
        Meter(metersize=110, padding=20, amountused=-2, labeltext="Poly",
                 meterstyle='warning.TLabel', metertype='semi', textfont=20).grid(row=7, column=6)

        # SEPARATOR PART
        
        # self.separator = ttk.Separator(bootstyle="info")
        # self.separator.grid(row=4, column=1, sticky="nsew", rowspan=2, columnspan=9)
        
        # PICKERS PART
        self.picker_row = 10 # to merge
        self.hours = tk.Label(self.master, text='HEURE', font=("bold", 20), pady=10)
        self.hours.grid(row=self.picker_row, column=1)

        self.pickertitle = tk.Label(self.master, text='PICKERS', font=("bold", 20), pady=10)
        self.pickertitle.grid(row=self.picker_row, column=4)

        # TOTALS PART
        self._totals = tk.Label(self.master, text='TOTALS', justify='center', font=('bold', 16), pady=10)
        self._totals.grid(row=23, column=4)

        self.totalprelev = tk.Label(self.master, text='Total \nPrelev', font=("bold", 13), pady=10)
        self.totalprelev.grid(row=24, column=3)

        self.deltacap = tk.Label(self.master, text='Delta \nCapacitif', font=("bold", 13), pady=10)
        self.deltacap.grid(row=24, column=4)

        self.totalpredprlv = tk.Label(self.master, text='Total \nPredic Prelev', font=("bold", 13), pady=10)
        self.totalpredprlv.grid(row=24, column=5)

        self.autoblock(self.lsofblock)


    def autohour(self):
        
        # mise à jour automatique après validation Bouton des chiffres: outout -> hourout, dictblockpickerout, totalpickerout
        #self.lines = [5,7,9,11,13,15,17,19]

        self.hour_row = 9 # to merge
        self.hourname = tk.Label(self.master, text="H", font=("bold", 13), padx=40, pady=10)
        self.hourout = tk.Listbox(self.master, height=1, width=25, justify="center")
        self.totalpickerout = tk.Listbox(self.master, height=1, width=5, justify="center")
        self.hourname.grid(row=self.hour_row, column=0)
        self.hourout.grid(row=self.hour_row, column=1)
        
        for nblock in self.listofcell:
            
            self.dictblockpickerout[self.listofcell.index(nblock)+1] = tk.Listbox(self.master, height=1, width=5, justify="center")
            self.dictblockpickerout[self.listofcell.index(nblock)+1].grid(row=self.hour_row, column=self.listofcell.index(nblock)+2)
            
            self.totalpickerout.grid(row=self.hour_row, column=self.listofcell.index(self.listofcell[-1])+4)

    # def autohour(self):
    #     self.count = 0
    #     # mise à jour automatique après validation Bouton des chiffres: outout -> hourout, dictblockpickerout, totalpickerout
    #     self.lines = [5,7,9,11,13,15,17,19]
    #     print(self.dict_hourout.keys())

    #     self.dict_hourname[self.count] = tk.Label(self.master, text="H{}".format(self.count), font=("bold", 13), padx=40, pady=10)
    #     self.dict_hourout[self.count]= tk.Listbox(self.master, height=1, width=25, justify="center")
    #     self.totalpickerout = tk.Listbox(self.master, height=1, width=5, justify="center")
    #     self.dict_hourname[self.count].grid(row=self.lines[self.count], column=0)
    #     self.dict_hourout[self.count].grid(row=self.lines[self.count], column=1)
        
    #     for nblock in self.listofcell:
            
    #         self.dictblockpickerout[self.listofcell.index(nblock)+1] = tk.Listbox(self.master, height=1, width=5, justify="center")
    #         self.dictblockpickerout[self.listofcell.index(nblock)+1].grid(row=self.lines[self.count], column=self.listofcell.index(nblock)+2)
            
    #         self.totalpickerout.grid(row=self.lines[self.count], column=self.listofcell.index(self.listofcell[-1])+4)
        
    #     return self.count

    def get_timepickeroutput(self, block_num):
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


    def add_ateanpik(self):
        self.dkey = ['time_glob', 'art_bck1', 'art_bck2', 'art_bck3', 'art_bck4', 'art_bck5', 'art_bck6', 'ean_bck1', 'ean_bck2', 'ean_bck3', 'ean_bck4', 'ean_bck5', 'ean_bck6', 'total_pickers']

        self.get_dictart = dict(zip(self.dkey[1:7], self.dictart_int.values()))
        self.get_dictart = dict((key, value.get()) for key, value in self.get_dictart.items())
        self.get_dictean = dict(zip(self.dkey[7:13], self.dictean_int.values()))
        self.get_dictean = dict((key, value.get()) for key, value in self.get_dictean.items())
        self.timerecord = datetime.datetime.now()
        self.get_dictglobalpick = {'time_glob': self.timerecord, **self.get_dictart,**self.get_dictean, 'total_pickers':self.totalpicker_text.get()}
               
        # if (self.get_dictglobalpick[key] == '' for key in self.get_dictglobalpick.keys()):
        #     tkinter.messagebox.showerror(
        #         "Required Fields", "Please include all fields")
        #     return
        #print(self.get_dictglobalpick[key] == '' for key in self.get_dictglobalpick.keys())

        # Insert into DB
        pdb.insert_gpick(self.get_dictglobalpick)
        #pdb.insert_poly(self.timerecord, self.totalpicker_text.get(), , )
            
        # Insert into list
        #self.hourout.insert(self.get_dictglobalpick['time_glob'])

        #     self.dictblockpickerout[self.lsofblock.index(nblock)].insert(self.dictart_int[self.lsofblock.index(nblock)].get(), self.dictean_int[self.lsofblock.index(nblock)].get(),
        #             self.totalpicker_text.get())
            #self.clear_text(nblock)
        self.get_timepickeroutput(len(self.listofcell))

    def autoblock(self, lsofblock):
        self.part_art_input = {}
        self.lsofblock = lsofblock
        
        for nblock in self.lsofblock:
            self.dictart_int[self.lsofblock.index(nblock)] = tk.IntVar()
            self.dictean_int[self.lsofblock.index(nblock)] = tk.IntVar()
            

            self.part_block = tk.Label(self.master, text=self.lsofblock[self.lsofblock.index(nblock)], font=("bold", 12))
            self.part_block.grid(row=1, column=self.lsofblock.index(nblock)+2)

            self.part_art_input[self.lsofblock.index(nblock)+1] = tk.Entry(self.master, textvariable=self.dictart_int[self.lsofblock.index(nblock)], justify="center", width=10)
            self.part_art_input[self.lsofblock.index(nblock)+1].grid(row=2, column=self.lsofblock.index(nblock)+2)

            self.part_ean_input = tk.Entry(self.master, textvariable=self.dictean_int[self.lsofblock.index(nblock)], justify="center", width=10)
            self.part_ean_input.grid(row=3, column=self.lsofblock.index(nblock)+2)

            Meter(metersize=130, padding=20, stripethickness=2, amountused=10, labeltext=self.lsofblock[self.lsofblock.index(nblock)], textappend='%',
                 meterstyle='success.TLabel').grid(row=22, column=self.lsofblock.index(nblock)+2)
            
            self.totalpicker = tk.Label(self.master, text='Total Pickers', font=("bold", 13), pady=10)
            self.totalpicker.grid(row=1, column=self.lsofblock.index(self.lsofblock[-1])+4)


    def totalpart(self):

        self.totalprelev_list = tk.Listbox(self.master, height=2, width=10, justify="center")
        self.totalprelev_list.grid(row=25, column=3)

        self.deltacap_list = tk.Listbox(self.master, height=2, width=10, justify="center")
        self.deltacap_list.grid(row=25, column=4)
        
        self.totalpredprlv_list = tk.Listbox(self.master, height=2, width=10, justify="center")
        self.totalpredprlv_list.grid(row=25, column=5)

    # def clear_text(self, nblocks):
    #     self.nblocks = nblocks
    #     self.part_art_input[self.nblocks].delete(0, tk.END)
    #     self.part_ean_input.delete(0, tk.END)


root = tk.Tk()
app = PickGAApp(listofcell=listofoutdoor, master=root)
style = Style('litera')
root = style.master
style.master.mainloop()
app.mainloop()