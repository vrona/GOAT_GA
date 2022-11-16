"""import tkinter as tk
from tkinter import ttk

class Gogoclass:
    def __init__(self):

        self.root = tk.Tk()
        self.root.title("bobo")
        self.root.geometry("500x500")

        mynotebook = ttk.Notebook(self.root)
        mynotebook.pack(pady=15)

        mytab1 = tk.Frame(mynotebook, width=500, height=500, bg='blue')
        mytab2 = tk.Frame(mynotebook, width=500, height=500, bg='red')

        mytab1.pack(fill="both", expand=1)
        mytab2.pack(fill="both", expand=1)

        mynotebook.add(mytab1, text="config")
        mynotebook.add(mytab2, text="task")

    def mainloop(self):
        self.root.mainloop()


bibi = Gogoclass()
bibi.mainloop()"""

import pandas as pd
import sqlite3

listdk = ['time_glob', 'total_pickers']
qualificatif = ["REAL PRIMARY KEY", "INTEGER", "NOT NULL"]
def creaglobalpick(numofblock):
    listart = ["artbck{}".format(nblock) for nblock in range(0, numofblock)] + ["eanbck{}".format(nblock) for nblock in range(0, numofblock)]
    for b in listart:
        gogo = ' '.join((b, qualificatif[1]))
        listart[listart.index(b)]= gogo
    
    # listart.insert(0, listdk[0])
    # listart.insert(len(listart), listdk[1])

    # df = pd.DataFrame(columns=listart)
    
    entete = "\"CREATE TABLE IF NOT EXISTS in_globalpick ("
    completone = ' '.join(('time_glob', qualificatif[0]))
    complettwo = ''.join((entete, completone))
    completthree = ', '.join((listart))
    completfour = ','.join((complettwo, completthree))
    
    completfive = ' '.join((listdk[1], qualificatif[1]))
    completsix = ', '.join((completfour, completfive))
    ending = ")\""
    completseven = entete + completone + ', ' + completthree + ', ' + completfive + ending

    
    #complet = ' '.join(((entete, ' '.join(listdk[0], qualificatif[0])))) #, k for k in listart, ' '.join(listdk[0], qualificatif[2]
    print(completseven)

    

creaglobalpick(2)