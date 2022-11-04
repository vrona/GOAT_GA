import tkinter as tk
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
bibi.mainloop()