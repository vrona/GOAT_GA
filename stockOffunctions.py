
"""concerning engine"""
# def insert_capatheo(self, dictcapat):
#     self.dictcapat = dictcapat
#     self.placeholder = ','.join(['?'] * len(self.dictcapat))
#     self.column = ', '.join(self.dictcapat.keys())
#     self.sql = "INSERT INTO %s (%s) VALUES (%s)" % ('in_capatheo', self.column, self.placeholder)
    
#     self.cur.execute(self.sql, list(self.dictcapat.values()))
#     self.conn.commit()

"""concerning backbone"""

"""concerning globaldb"""
def insert_totals_out(self, id, timeofrecord, total_prelev, delta_capacitif, total_predic, capareal_h, capaavg):
    self.cur.execute("INSERT INTO totals_out VALUES (?,?,?,?,?,?,?)",(id, timeofrecord, total_prelev, delta_capacitif, total_predic, capareal_h, capaavg))
    self.conn.commit()

def insert_block_picker_out(self, id, timeofrecord, block_id_origin, block_id_landing, picker):
    self.cur.execute("INSERT INTO block_picker_out VALUES (?,?,?,?,?)",(id, timeofrecord, block_id_origin, block_id_landing, picker))
    self.conn.commit()

def insert_capatheo(self, capatheo_h):
    self.cur.execute("INSERT INTO capa VALUES (?)",(capatheo_h,))
    self.conn.commit()


def insert_poly(self, time_glob, total_picker_onsite):
    self.cur.execute("INSERT INTO poly_out VALUES (?,?)",(time_glob, total_picker_onsite))
    self.conn.commit()

"""concerning activity"""
def get_goal(self):
    pdb = UsingDB("./database/goatdata.db")
    for ba, rowa, rowe in zip(range(0, len(globaldb.ls_goal_g)//2), pdb.fetch_artgoal(), pdb.fetch_eangoal()):
        self.artgoal_input[ba].insert(tk.END, rowa)
        self.eangoal_input[ba].insert(tk.END, rowe)

def get_timepickeroutput(self, block_num):
    pdb = UsingDB("./database/goatdata.db")
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

def autohour(self):
        
    # mise à jour automatique après validation Bouton des chiffres: outout -> hourout, dictblockpickerout, totalpickerout
    #self.lines = [5,7,9,11,13,15,17,19]

    self.hour_row = 9 # to merge
    self.hourname = tk.Label(self.master, text="H", font=("bold", 13), padx=40, pady=10)
    self.hourout = tk.Listbox(self.master, height=1, width=25, justify="center")
    self.totalpickerout = tk.Listbox(self.master, height=1, width=5, justify="center")
    self.hourname.grid(row=self.hour_row, column=0)
    self.hourout.grid(row=self.hour_row, column=1)
    
    for nblock in adminblocks.mainlistblock:
        
        self.dictblockpickerout[adminblocks.mainlistblock.index(nblock)] = tk.Listbox(self.master, height=1, width=5, justify="center")
        self.dictblockpickerout[adminblocks.mainlistblock.index(nblock)].grid(row=self.hour_row, column=adminblocks.mainlistblock.index(nblock)+2)
        
        self.totalpickerout.grid(row=self.hour_row, column=adminblocks.mainlistblock.index(adminblocks.mainlistblock[-1])+4)

    #pdb.insert_poly(self.timerecord, self.totalpicker_text.get(), , )
        
    # Insert into list
    #self.hourout.insert(self.get_dictglobalpick['time_glob'])

    #     self.dictblockpickerout[self.lsofblock.index(nblock)].insert(self.dictart_int[self.lsofblock.index(nblock)].get(), self.dictean_int[self.lsofblock.index(nblock)].get(),
    #             self.totalpicker_text.get())
        #self.clear_text(nblock)