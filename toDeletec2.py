from tkinter import *
#from db import Database

#db = Database('store.db')

"""def show_me(app):
        # Parts List (Listbox)
    parts_list = Listbox(app, height=8, width=50, border=0)
    parts_list.grid(row=10, column=0, columnspan=3, rowspan=6, pady=20, padx=20)

    parts_list.delete(0, END)
    for row in db.fetch():
        parts_list.insert(END, row)
"""
def add_block() :
    print("Add")

def remove_block():
    print("remove")

def rename_block():
    print("rename")

def autoblock(app, outdoor):
    
    dictartentry = {}
    dicteanentry = {}
    lsofblock = outdoor

    for b in outdoor :
        dictartentry[lsofblock.index(b)] = IntVar()
        dicteanentry[lsofblock.index(b)] = IntVar()
        part_block = Label(app, text=lsofblock[lsofblock.index(b)], font=("bold", 13), pady=10)
        part_block.grid(row=1, column=lsofblock.index(b)+1)

        part_art_entry = Entry(app, textvariable=dictartentry[lsofblock.index(b)], justify="center", width=10)
        part_art_entry.grid(row=2, column=lsofblock.index(b)+1)

        part_ean_entry = Entry(app, textvariable=dicteanentry[lsofblock.index(b)], justify="center", width=10)
        part_ean_entry.grid(row=3, column=lsofblock.index(b)+1)


def blockc2(listofblock):
    app = Tk()

    app.title("GOAT Of GA")
    app.geometry("1080x750")
    
    part_picker_text = StringVar()
    part_renameb_text = StringVar()
    
    #part_block = Label(app, text='BLOCKS', justify='center', font=("bold", 14), pady=10)
    #part_block.grid(row=0, column=3)

    part_article = Label(app, text='Articles', font=("bold", 13), pady=10)
    part_article.grid(row=2, column=0)

    part_ean = Label(app, text='EAN', font=("bold", 13), pady=10)
    part_ean.grid(row=3, column=0)

    part_picker = Label(app, text='DKT Pickers', font=("bold", 13), pady=10)
    part_picker.grid(row=4, column=0)

    part_picker_entry = Entry(app, textvariable=part_picker_text, justify="center", width=10)
    part_picker_entry.grid(row=4, column=1)

    autoblock(app, listofblock)

    add_btn = Button(app, text="Ajouter Block", justify="center", width=14, command=add_block)
    add_btn.grid(row=400, column=1, pady=10)

    add_btn = Button(app, text="Supprimer Block", justify="center", width=14, command=remove_block)
    add_btn.grid(row=400, column=2, pady=10)

    add_btn = Button(app, text="Renommer Block", justify="center", width=14, command=rename_block)
    add_btn.grid(row=400, column=3, pady=10)

    part_ean_entry = Entry(app, textvariable=part_renameb_text, justify="center", width=10)
    part_ean_entry.grid(row=401, column=3)


    #show_me(app)
    
    app.mainloop()
