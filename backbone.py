import tkinter as tk
from tkinter import ttk
from adminblocks import Blocks
import adminblocks
from activity import Activity
from PIL import Image, ImageTk
from ttkbootstrap import Style
from ttkbootstrap.constants import *

import os

class PickGAApp(tk.Frame):
    
    def __init__(self, master):
        super().__init__(master)

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
        self.validblock_btn = ttk.Button(self.admin, text="Valider\n Configuration", bootstyle="danger", command=lambda:[Blocks(self.admin).validate_block(),self.ready(), self.switchstate()], width=12)
        self.validblock_btn.grid(row=30, column=1, pady=10)

        self.launch_btn = ttk.Button(self.admin, text="Lancer Activité", style='valid.btn', width=12, command=lambda:self.selecttab(1), state=tk.DISABLED)
        self.launch_btn.grid(row=30, column=2, padx=5)

        Blocks(self.admin) # admin tab widget

        #Configtab(self.config).configwidget(self.selecttab)
        self.credit_widget()

        # Button killing app
        self.unlock_img = Image.open("./logo/unlock.png")
        self.resized_img= self.unlock_img.resize((15,15))
        self.img = ImageTk.PhotoImage(self.resized_img)
        self.unlock_var = tk.IntVar()
        self.unlock_btn = ttk.Checkbutton(self.activity, text="Unlock", variable=self.unlock_var, bootstyle="danger-round-toggle", image=self.img, command=self.unlock_killbtn)
        #self.unlock_btn = ttk.Checkbutton(self.activity, text="Unlock", variable=self.unlock_var, bootstyle="danger-round-toggle", image=self.img, command=self.unlock_killbtn)
        self.unlock_btn.grid(row=33, column=1)
        self.reset_btn = ttk.Button(self.activity, text="Reset App", comman=self.resetapp, bootstyle="danger", state=tk.NORMAL)
        #self.reset_btn = ttk.Button(self.activity, text="Reset App", comman=self.resetapp, bootstyle="danger", state=tk.DISABLED)
        self.reset_btn.grid(row=34, column=1, pady=5)

    def resetapp(self):
        if os.path.exists("./database/goatdata.db"):
            os.remove("./database/goatdata.db")
            print("DB removed")
        else:
            print("The file does not exist")
        
        self.root.destroy()

    def unlock_killbtn(self):

        if self.unlock_var.get() == 1:
            self.reset_btn["state"] = tk.NORMAL
        else:
            self.reset_btn['state'] = tk.DISABLED
    
    def switchstate(self):
        self.launch_btn["state"]=tk.NORMAL
        self.validblock_btn["state"]=tk.DISABLED

    def ready(self):
        Activity(self.activity).task_widget(adminblocks.mainlistblock)

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