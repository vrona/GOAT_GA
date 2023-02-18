import tkinter as tk
from tkinter.ttk import *
import tkinter.messagebox
from globaldb import CreationDB


is_on = False
mainlistblock = ["C_Chasse", "C_Pêche", "C_SportCo", "D_Glisse", "D_Running", "E_Rando_Camp", "E_Prio", "V_Cycle_Urban", "V_Prio", "PFECA", "Implant"]
speedtheodict = {"C_Chasse":270, "C_Pêche":290 , "C_SportCo":290, "D_Glisse":306, "D_Running":290, "E_Rando_Camp":220, "E_Prio":220, "V_Cycle_Urban":220, "V_Prio":220, "PFECA":220, "Implant":220}
setthegoal = [None] *2

class Blocks(tk.Frame):
    
    
    def __init__(self, master):

        self.master = master
        self.index_selec = []
        self.index_name = []
        self.dicts_select = {}
        self.target_input = tk.IntVar()
        self.percent_input = tk.IntVar()
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


        self.intro_label = tk.Label(self.master, text="Configuration de l'activité", justify='center',font=('bold', 20))
        self.text_label = Label(self.master, text="Pour ajouter, supprimer ou renommer les blocks,\nselectionner les.\n\nTu connais l'objectif du jour ?\nOui, renseignes le Pilotage du jour en VOLUME ou en %.\nNon, demande à ton patron, ta patronne.\n\nPuis valides et lances l'activité.", font=18, padding=10)
        self.intro_label.place(x=550,y=25) #.grid(row=0, column=1, columnspan=3)
        self.text_label.place(x=550,y=75) #.grid(row=1, column=1, columnspan=3)

        # SEPARATOR PART
        self.blocksepleft = Separator(self.master, bootstyle="success", orient="horizontal")
        self.blocksepleft.grid(row=2, column=0, sticky="nsew", columnspan=4)
        self.blockpart = Label(self.master, text="BLOCKS", justify='center', font=('bold', 16))
        self.blockpart.grid(row=2, column=2, pady=15)
        self.blocksepright = Separator(self.master, bootstyle="success")
        self.blocksepright.grid(row=2, column=3, sticky="nsew", columnspan=4)
        
        self.listblocktitle = Label(self.master, text="Liste de Blocks", font=('bold', 16)) #, padding=15
        self.listblocktitle.grid(row=3, column=0)
        self.blocks_list = tk.Listbox(self.master, selectmode= "multiple", height=10, width=13, font=18) #, 
        self.blocks_list.place(x=10,y=75) #padx=20, rowspan=3, columnspan=2 grid(row=4, column=1, pady=15)  #

        # Add Remove Blocks
        self.blocks_label = Label(self.master, text="Nom Block", justify='center', font=('bold', 14))
        self.blocks_label.grid(row=3, column=2) #.place(x=203,y=165) #
        
        self.blocks_entry = tk.Entry(self.master, textvariable=self.blocks_text,justify='center')
        self.blocks_entry.grid(row=4, column=2)

        self.add_btn = Button(self.master, text="Ajouter Block", bootstyle="success", width=12, command=self.add_block)
        self.add_btn.grid(row=6, column=2, pady=5)

        self.remove_btn = Button(self.master, text="Supprimer Block", bootstyle="warning", width=12, command=self.remove_block)
        self.remove_btn.grid(row=7, column=2, pady=15)

        # Changing Block
        self.oldblocks_label = tk.Label(self.master, text="Ancien Nom Block\n(à sélectionner)", justify='center', font=16)
        self.oldblocks_label.grid(row=12, column=2, pady=15)

        self.newblocks_label = tk.Label(self.master, text="Nouveau Nom Block", justify='center', font=16)
        self.newblocks_label.grid(row=14, column=2, pady=5)

        self.oldblocks_entry = tk.Entry(self.master, textvariable=self.oldblocks_text, justify='center')
        self.oldblocks_entry.grid(row=13, column=2)

        self.newblocks_entry = tk.Entry(self.master, textvariable=self.newblocks_text, justify='center')
        self.newblocks_entry.grid(row=15, column=2)

        self.rename_btn = Button(self.master, text="Renommer Block", bootstyle="info", width=12,command=self.replace_block)
        self.rename_btn.grid(row=16, column=2, pady=10)

        # SEPARATOR PART
        self.pilotsepleft = Separator(self.master, bootstyle="success")
        self.pilotsepleft.grid(row=17, column=0, sticky="nsew", columnspan=4)
        self.pilotpart = Label(self.master, text="PILOTAGE", justify='center', font=('bold', 16))
        self.pilotpart.grid(row=17, column=2, pady=15)
        self.pilotsepright = Separator(self.master, bootstyle="success")
        self.pilotsepright.grid(row=17, column=3, sticky="nsew", columnspan=4)

        # PILOTAGE PART
        self.volume = "Volume Art."
        self.percentage = "Pourcent. %"
        self.volbtn = Button(self.master, text=self.volume, command=self.switch_vp, bootstyle="success-outline") #bootstyle="success-round-toggle", 
        self.volbtn.grid(row=20, column=2) #place(x=180, y=440) #

        self.target_label = Label(self.master, text="Goal Vol. Tablette Art.", justify='center', font=16)
        self.target_label.grid(row=21, column=2, pady=25)
        self.target_entry = tk.Entry(self.master, textvariable=self.target_input, justify='center')
        self.target_entry.grid(row=22, column=2)

        self.percent_label = Label(self.master, text="Goal % Tablette Art.", justify='center', font=16)
        self.percent_label.grid(row=25, column=2, pady=10)
        self.percent_entry = tk.Entry(self.master, textvariable=self.percent_input, justify='center', state=tk.DISABLED)
        self.percent_entry.grid(row=26, column=2)

        # Pilotage Validation Button
        self.validblock_btn = Button(self.master, text="Valider Pilotage", bootstyle="danger", command=self.goalpick, width=12)
        self.validblock_btn.grid(row=27, column=2, pady=10)

        # SEPARATOR PART
        self.validsepleft = Separator(self.master, bootstyle="success")
        self.validsepleft.grid(row=28, column=0, sticky="nsew", columnspan=4)
        self.validpart = Label(self.master, text="GO LIVE", justify='center', font=('bold', 16))
        self.validpart.grid(row=28, column=2, pady=15)
        self.validsepright = Separator(self.master, bootstyle="success")
        self.validsepright.grid(row=28, column=3, sticky="nsew", columnspan=4)

        # Bind select
        self.blocks_list.bind('<<ListboxSelect>>', self.select_item)


    def goalpick(self):
        
        setthegoal[0] = self.target_input.get()
        setthegoal[1] = self.percent_input.get()

        if self.target_input.get() > 0 and self.percent_input.get() > 0: 
            tkinter.messagebox.showerror(
                "Champs requis", "Soit Vol., soit Percent ou les 2 à zéro, svp")
            return

    def switch_vp(self):
        global is_on

        if is_on:
            self.volbtn.config(text=self.percentage)        
            self.target_entry['state']=tk.DISABLED
            self.percent_entry['state']=tk.NORMAL
            is_on = False
            
        else: 
            self.volbtn.config(text=self.volume)
            self.target_entry['state']=tk.NORMAL
            self.percent_entry['state']=tk.DISABLED
            is_on = True

    def add_block(self):
        if self.blocks_text.get() == '':
            tkinter.messagebox.showerror(
                "Champs requis", "Selectionnez un nom de la liste, svp")
            return
        elif self.blocks_text.get() in mainlistblock:
            tkinter.messagebox.showerror(
                "Attention", "Ce nom existe déjà. ;-)")
            return
        else:
            mainlistblock.append(self.blocks_text.get())
            speedtheodict[self.blocks_text.get()] = 200

        self.clear_text()
        self.show_block()

    def remove_block(self):
        if self.blocks_text.get() == '':
            tkinter.messagebox.showerror(
                "Champs requis", "Selectionnez un nom de la liste, svp")
            return
                    
        else:
           
            for key, value in self.dicts_select.items():

                mainlistblock.remove(value)
                speedtheodict.pop(value)
                self.index_selec.remove(key)
    
            self.dicts_select.clear()

        self.clear_text()
        self.show_block()

    def replace_block(self):
        if self.oldblocks_text.get() == '' or self.newblocks_text.get() == '':
            tkinter.messagebox.showerror(
                "Champs requis, Ancien nom ou Nouveau nom à remplir, svp.")
            return

        self.indexold = mainlistblock.index(self.oldblocks_text.get())
        mainlistblock[self.indexold] = self.newblocks_text.get()
        speedtheodict[self.newblocks_text.get()]  = speedtheodict.pop(self.oldblocks_text.get())
        self.clear_text()
        self.show_block()

    def iniblock(self, listofblock):
        self.listofblock = listofblock
        for data in self.listofblock:
            
            self.pdb.insert_nameblock(self.listofblock.index(data)+1, "{}".format(data))


    def validate_block(self):
        global mainlistblock, speedtheodict, setthegoal
        #self.listofids = list(mainlistblock.index(x) for x in mainlistblock)
        #self.data = {'id': self.listofids, 'name': mainlistblock}
        #self.df = pd.DataFrame(self.data, columns=['id','name'])
        self.pdb = CreationDB(len(mainlistblock)) #,"./database/goatdata.db"
        
        # speedtheodict["speedthavg"] = sum(speedtheodict.values()) / len(speedtheodict) # TO ADD LATER
        
        self.iniblock(mainlistblock)

        self.add_btn['state']=tk.DISABLED
        self.remove_btn['state']=tk.DISABLED
        self.oldblocks_entry['state']=tk.DISABLED
        self.newblocks_entry['state']=tk.DISABLED
        self.rename_btn['state']=tk.DISABLED
        self.target_entry['state']=tk.DISABLED
        self.percent_entry['state']=tk.DISABLED

    def clear_text(self):
        self.blocks_entry.delete(0, tk.END)
        self.oldblocks_entry.delete(0, tk.END)
        self.newblocks_entry.delete(0, tk.END)

    def select_item(self, event):
        
        try:
            # Get index
            #index = self.blocks_list.curselection()
            self.index_selec = list(self.blocks_list.curselection())

            self.dicts_select = dict(zip(self.index_selec, list(mainlistblock[x] for x in self.index_selec)))
            #print(x for x in self.index_selec)
            #self.index_name.append(index)
        
            for idx in self.index_selec:
        
            # Get selected item
                self.selected_item = self.blocks_list.get(idx)

            # Add text to entries
                self.blocks_entry.delete(0, tk.END)
                self.blocks_entry.insert(tk.END, self.selected_item)
                self.oldblocks_entry.delete(0, tk.END)
                self.oldblocks_entry.insert(tk.END, self.selected_item)
            # print(self.index_selec)
            # print(self.index_name)
        except IndexError:
            pass
