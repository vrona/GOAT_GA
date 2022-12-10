
"""concerning engine"""

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