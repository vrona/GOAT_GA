"""ttkbootstrap demo"""
# python -m ttkbootstrap

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

"""concerning dispatch"""
def bankofpicker(self): # MOTEUR DE DISPATCH BASE SUR LE RESTANT

    a= self.pkrandpoly()
    
    self.df_declaredtp = pd.read_sql_query("SELECT total_pickers FROM in_globalpick ORDER BY id DESC LIMIT 1", self.conn)
    self.declaredtp = self.df_declaredtp.iloc[-1][0]
    
    listofname = list("Picker_%s"%(x) for x in range(self.declaredtp))

    while bool(a[0]):
        max_needed_pickr_value = max(a[0].values())
        max_needed_pickr_key = max(a[0], key=a[0].get)

        self.block_list[max_needed_pickr_key] = []

        #self.split_pickr(self.block_list[max_needed_pickr_key], max_needed_pickr_value, listofname)
        while listofname:

            if max_needed_pickr_value >= 1:
                self.block_list[max_needed_pickr_key].append((listofname[0], 1))
                listofname.pop(listofname.index(listofname[0]))
                max_needed_pickr_value -= 1

            if max_needed_pickr_value < 1:
                self.block_list_buffer[max_needed_pickr_key] = max_needed_pickr_value
                max_needed_pickr_value -= max_needed_pickr_value


                #print(round(float(sum(self.block_list_buffer.values())), 2))
                
                # if threshold < 0.51:
                #     if not listofbuffer:
                        
                #         listofbuffer.append(listofname[0])
                #         self.block_list[max_needed_pickr_key].append(((listofname[0]), round(float(max_needed_pickr_value), 2)))
                #         listofname.pop(listofname.index(listofname[0]))
                #         max_needed_pickr_value -= max_needed_pickr_value
                                        
                #     else:
                #         self.block_list[max_needed_pickr_key].append(((listofbuffer[0]), round(float(max_needed_pickr_value), 2)))
                #         max_needed_pickr_value -= max_needed_pickr_value

                # elif threshold > 0.51:
                #     listofbuffer.append(listofname[0])
                #     self.block_list[max_needed_pickr_key].append(((listofbuffer[-1]), round(float(max_needed_pickr_value), 2)))
                #     max_needed_pickr_value -= max_needed_pickr_value
                break

        a[0].pop(max_needed_pickr_key)
    echoof = self.block_list_buffer.values()
    CombPicker(echoof, 1)
    # for kval, vval in self.block_list_buffer.items():
    #     self.block_list[kval].append((listofname[0], vval))

    #print(self.block_list, '\n',self.block_list_buffer, '\n',listofname)

     a = {"A": 2.83, "B": 1.12, "C": 1.05}
        blocklist = {}

        while a:

            max_value = max(a.values())
            max_key = max(a, key=a.get)

            blocklist[max_key] = []
            time = 0

            fullpicker = []
            
            while time < sum(a.values()):

                picker_stock = {"Picker%s"% (x):1 for x in range(int(sum(a.values())))}

                #max_splited_picker = max(picker_stock.values())
                #max_splited_picker_key = max(picker_stock, key=picker_stock.get)
                #max_picker = [pickr for pickr, value in picker_stock.items() if value == max(picker_stock.values())]

                randome = random.sample(picker_stock.items(), 1)

                max_splited_picker = max(picker_stock.values())
                max_splited_picker_key = max(picker_stock, key=picker_stock.get)
                
                if max_value >= picker_stock[randome[0][0]]:

                    blocklist[max_key].append((randome[0][0], randome[0][1]))

                    picker_stock.pop(randome[0][0])
                    max_value -= 1
                    time += 1

                if max_value < max_splited_picker :
                    if max_splited_picker == 0 :
                        break
                    #picker_stock.pop(max_splited_picker_key) 
                    #print(max_splited_picker, max_splited_picker_key)
                    else:
                        blocklist[max_key].append((max_splited_picker_key, max_value))
                        picker_stock[max_splited_picker_key] = picker_stock[max_splited_picker_key] - max_value
                        
                        time += max_value
                        #max_value -= max_value
                        if picker_stock[max_splited_picker_key] == 0:
                            picker_stock.pop(max_splited_picker_key)

            


            a.pop(max_key)
        print(blocklist)


global ls_task_data, prev_dicttask

        self.dicttask = dicttask
        pre_set = set(prev_dicttask.keys())
        new_set = set(self.dicttask.keys()) # .items()
        
        if len(ls_task_data) == 0:
            sql_task = []

            ls_task_data = ["{}_{}_data".format(ktask, ndata) for ktask, vpicker in self.dicttask.items() for ndata in range(len(vpicker))]
            ls_human = ["{}_{}_human".format(ktask, ndata) for ktask, vpicker in self.dicttask.items() for ndata in range(len(vpicker))]

            for task_data in ls_task_data:
                self.attrib_task = " ".join((task_data, "FLOAT"))
                sql_task.append(self.attrib_task)
            
            for task_human in ls_human:
                self.attrib_task = " ".join((task_human, "VARCHAR"))
                sql_task.append(self.attrib_task)

            # Table 8 input prop of time per blocks (aka task_table)
            self.begintask = "CREATE TABLE IF NOT EXISTS task_table ("
            self.bodytask = ", ".join((sql_task))
            self.completedtask = self.begintask+"id INTEGER PRIMARY KEY, "+self.bodytask+")"
            self.conn = sqlite3.connect(db)
            self.cur = self.conn.cursor()

            self.cur.execute(self.completedtask)

            prev_dicttask = self.dicttask # updating previous dict of tasks

            self.placeholder = ','.join(['?'] * len(sql_task))
            self.column = ', '.join(sql_task)

            self.sql = "INSERT INTO %s (%s) VALUES (%s)" % ('task_table', self.column, self.placeholder)
            print(self.sql, '\n')
            print(self.dicttask, '\n')
            print([task_data for vpicker in self.dicttask.values() for task_data in vpicker]) #DEAD DEAD DEAD
            
            self.cur.execute(self.sql, list(task_data for vpicker in self.dicttask.values() for task_data in vpicker))
            self.conn.commit()

        else: #len(ls_task_data) != previous_lstask
            sql_addtask = []
            self.add_dict = pre_set ^ new_set # searching differences between keys
            print(type(self.add_dict), self.add_dict)
            buffer_task = [k for k in self.add_dict.keys()]
            for addtask_block in buffer_task:
                self.add_attrib_task = " ".join((addtask_block, "FLOAT"))
                sql_addtask.append(self.add_attrib_task)
            
            self.add_begintask = "ALTER TABLE task_table"
            self.add_bodytask = ", ".join((sql_addtask))
            self.add_completedtask = self.add_begintask+" ADD "+ self.add_bodytask
            self.conn = sqlite3.connect(db)
            self.cur = self.conn.cursor()
            self.cur.execute(self.add_completedtask)

            self.placeholder = ','.join(['?'] * len(self.dicttask))
            self.column = ', '.join(self.dicttask.keys())
            self.sql = "INSERT INTO %s (%s) VALUES (%s)" % ('task_table', self.column, self.placeholder)

            self.cur.execute(self.sql, list(self.dictbase.values()))
            self.conn.commit()

            prev_dicttask = self.dicttask # updating previous dict of tasks
     
        
