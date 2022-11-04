import tkinter as tk
import tkinter.messagebox
from tkinter import ttk
from pickdb import PickingDB
from PIL import Image, ImageTk
from gauge import Meter
from ttkbootstrap import Style


listofoutdoor = ["Sport_Co", "Chasse", "Glisse", "Running", "Implant"]
pdb = PickingDB("localstorage.db")

class PickGAApp(tk.Frame):

    def __init__(self, master, listofcell):
        super().__init__(master)
        self.dictblocklist = {}
        self.master = master
        self.listofcell = listofcell
        master.title("GOAT Of GA (alpha)")
        master.geometry("1300x1080")
        #master.resizable(False, False)
        self.backgd()
        self.block_widget(self.listofcell)
        self.autohour()
        self.totalpart()
       
        #self.selected_item = 0
        self.get_picker(0)
    
    def backgd(self):
        self.imagecestas = Image.open("LogoCestasDC2024.png")
        self.resized_image= self.imagecestas.resize((121,100))
        self.test = ImageTk.PhotoImage(self.resized_image)
        self.label1 = tkinter.Label(image=self.test)
        self.label1.image = self.test

        self.label1.place(x=10, y=800)

        
    def get_picker(self, block_id):
        self.block_id = block_id
        self.block = self.block_id +1 
        self.dictblocklist[self.block_id].delete(0, tk.END)
        for row in pdb.fetch_picker(self.block):
            self.dictblocklist[self.block_id].insert(tk.END, row)
        

    def block_widget(self, lsofblock):
        self.lsofblock = lsofblock

        self.totalpicker_text = tk.IntVar()

        self._block = tk.Label(self.master, text='BLOCKS', justify='center', font=("bold", 14), pady=10)
        self._block.grid(row=0, column=4)

        self._article = tk.Label(self.master, text='Articles', font=("bold", 13), pady=10)
        self._article.grid(row=2, column=1)

        self.ean = tk.Label(self.master, text='EAN', font=("bold", 13), pady=10)
        self.ean.grid(row=3, column=1)

        self.hours = tk.Label(self.master, text='HOURS', font=("bold", 14), pady=10)
        self.hours.grid(row=4, column=1)

        self.pickertitle = tk.Label(self.master, text='PICKERS', font=("bold", 14), pady=10)
        self.pickertitle.grid(row=4, column=4)

        self.totalpicker = tk.Label(self.master, text='Total Pickers', font=("bold", 13), pady=10)
        self.totalpicker.grid(row=1, column=9)

        self.totalpicker_entry = tk.Entry(self.master, textvariable=self.totalpicker_text, justify="center", width=10)
        self.totalpicker_entry.grid(row=2, column=9)

        self.totalprelev = tk.Label(self.master, text='Total \nPrelev', font=("bold", 13), pady=10)
        self.totalprelev.grid(row=4, column=9)

        self.totalpredprlv = tk.Label(self.master, text='Delta \nCapacitif', font=("bold", 13), pady=10)
        self.totalpredprlv.grid(row=4, column=11)

        self.deltacap = tk.Label(self.master, text='Total \nPredic Prelev', font=("bold", 13), pady=10)
        self.deltacap.grid(row=4, column=13)

        """self.add_btn = tk.Button(
            self.master, text="Enregistrer", width=12, command=self.add_item)
        self.add_btn.grid(row=3, column=14, pady=20)"""

        self.autoblock(self.lsofblock)


    def autohour(self):
        self.lines = [5,7,9,11,13,15,17,19]
        
        for hours in range(0, 8):
            self.hourrec = tk.Label(self.master, text="H{}".format(hours), font=("bold", 13), padx=40, pady=10)
            self.hourrec.grid(row=self.lines[hours], column=0)
            
    

    def autoblock(self, lsofblock):
        self.dictartentry = {}
        self.dicteanentry = {}
        
        self.lsofblock = lsofblock
        
        for nblock in self.lsofblock:
            print(nblock)
            self.dictartentry[self.lsofblock.index(nblock)] = tk.IntVar()
            self.dicteanentry[self.lsofblock.index(nblock)] = tk.IntVar()
            self.dictblocklist[self.lsofblock.index(nblock)] = tk.Listbox(self.master, height=2, width=10, border=1)

            self.part_block = tk.Label(self.master, text=self.lsofblock[self.lsofblock.index(nblock)], font=("bold", 12))
            self.part_block.grid(row=1, column=self.lsofblock.index(nblock)+2)

            self.part_art_entry = tk.Entry(self.master, textvariable=self.dictartentry[self.lsofblock.index(nblock)], justify="center", width=10)
            self.part_art_entry.grid(row=2, column=self.lsofblock.index(nblock)+2)

            self.part_ean_entry = tk.Entry(self.master, textvariable=self.dicteanentry[self.lsofblock.index(nblock)], justify="center", width=10)
            self.part_ean_entry.grid(row=3, column=self.lsofblock.index(nblock)+2)

            Meter(metersize=130, padding=20, stripethickness=2, amountused=10, labeltext=self.lsofblock[self.lsofblock.index(nblock)], textappend='%',
                meterstyle='success.TLabel').grid(row=22, column=self.lsofblock.index(nblock)+2)
            
            self.dictblocklist[self.lsofblock.index(nblock)].grid(row=5, column=self.lsofblock.index(nblock)+2)

            self.get_picker(self.lsofblock.index(nblock))


    def totalpart(self):

        self.h_hour = tk.Listbox(self.master, height=2, width=10, border=1)
        self.h_hour.grid(row=4, column=1)

        self.total_list = tk.Listbox(self.master, height=2, width=10, border=1)
        self.total_list.grid(row=5, column=9)

        self.total_list = tk.Listbox(self.master, height=2, width=10, border=1)
        self.total_list.grid(row=5, column=11)
        
        self.total_list = tk.Listbox(self.master, height=2, width=10, border=1)
        self.total_list.grid(row=5, column=13)

    """def add_item(self):
        if self.dictartentry[self.lsofblock.index(nblock)].get() == '' or self.dicteanentry[self.lsofblock.index(nblock)].get() == '' or self.totalpicker_text.get() == '':
            tkinter.messagebox.showerror(
                "Required Fields", "Please include all fields")
            return
        print(self.part_text.get())
        # Insert into DB
        pdb.insert(self.self.dictartentry[self.lsofblock.index(nblock)].get(), self.dicteanentry[self.lsofblock.index(nblock)].get(),
                  self.totalpicker_text.get())
        # Clear list
        self.parts_list.delete(0, tk.END)
        # Insert into list
        self.parts_list.insert(tk.END, (self.part_text.get(), self.customer_text.get(
        ), self.retailer_text.get(), self.price_text.get()))
        self.clear_text()"""

    def clear_text(self):
        self.part_art_entry.delete(0, tk.END)
        self.part_ean_entry.delete(0, tk.END)


root = tk.Tk()
app = PickGAApp(listofcell=listofoutdoor, master=root)
style = Style('litera')
root = style.master
style.master.mainloop()
app.mainloop()