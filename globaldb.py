import sqlite3
import time

lsartean = []
ls_goal_g = []
ls_w_artean = []
ls_speed_artean = []
ls_delta = []
ls_total = []
ls_task_data = []
prev_dicttask = {}

def helper_dbtype(listofsth, datatype):
    listofall = []

    for data in listofsth:
        attribute = " ".join((data, datatype))
        listofall.append(attribute)
    return listofall


class CreationDB:
    def __init__(self, numofblock, db="./database/input_data.db"):
        self.dictbase = {}
        self.numofblock = numofblock
        self.conn = sqlite3.connect(db)
        self.cur = self.conn.cursor()
        self.createglobalpick(self.numofblock, db)
        self.cur.execute("CREATE TABLE IF NOT EXISTS blocks_in (block_id INTEGER PRIMARY KEY, name text NOT NULL)")
        
        #self.cur.execute("CREATE TABLE IF NOT EXISTS block_picker_out (block_id PRIMARY KEY, num_picker INTEGER, total_picker INTEGER, FOREIGN KEY (block_id) REFERENCES blocks_in (id), FOREIGN KEY (total_picker) REFERENCES in_globalpick (total_pickers))")
        #self.cur.execute("CREATE TABLE IF NOT EXISTS poly_out (time_glob REAL PRIMARY KEY, total_picker_onsite INTEGER NOT NULL, total_pick_goal INTEGER NOT NULL, poly_status INTEGER, FOREIGN KEY (total_picker_onsite) REFERENCES in_globalpick (time_glob), FOREIGN KEY (time_glob) REFERENCES in_globalpick (total_pickers))")
        self.createtotalpick(self.numofblock, db)
        
        self.conn.commit()

    def createglobalpick(self, numofblock, db):
        global lsartean, ls_goal_g, ls_delta, ls_speed_artean

        self.numoblock = numofblock
        
        lsartean = ["artbck{}".format(nblock) for nblock in range(0, self.numofblock)] + ["eanbck{}".format(nblock) for nblock in range(0, self.numofblock)]
        ls_goal_g = ["goal_artbck{}".format(nblock) for nblock in range(0, self.numofblock)] + ["goal_eanbck{}".format(nblock) for nblock in range(0, self.numofblock)]
        ls_w_artean = ["wartbck{}".format(nblock) for nblock in range(0, self.numofblock)] + ["weanbck{}".format(nblock) for nblock in range(0, self.numofblock)] + ["ratioaebck{}".format(nblock) for nblock in range(0, self.numofblock)]
        ls_speed_artean = ["speed_artbck{}".format(nblock) for nblock in range(0, self.numofblock)] + ["speed_eanbck{}".format(nblock) for nblock in range(0, self.numofblock)] + ["speed_goal_artbck{}".format(nblock) for nblock in range(0, self.numofblock)] + ["speed_goal_eanbck{}".format(nblock) for nblock in range(0, self.numofblock)]
        ls_delta = ["delta_artbck{}".format(nblock) for nblock in range(0, self.numofblock)] + ["delta_eanbck{}".format(nblock) for nblock in range(0, self.numofblock)]

        
        sql_ent = helper_dbtype(lsartean, "INTEGER")
        sql_ent_g = helper_dbtype(ls_goal_g, "INTEGER")
        sql_w_ent = helper_dbtype(ls_w_artean, "FLOAT")
        sql_speed = helper_dbtype(ls_speed_artean, "FLOAT")
        sql_delta = helper_dbtype(ls_delta, "INTEGER")

        # Table 1 input vol article ean
        self.entete = "CREATE TABLE IF NOT EXISTS in_globalpick ("
        self.corps = ", ".join((sql_ent))
        self.complete = self.entete+"id INTEGER PRIMARY KEY, time_glob REAL, "+self.corps+", total_pickers INTEGER)"

        # Table 2 computed goal article ean
        self.entete_g = "CREATE TABLE IF NOT EXISTS goalpick ("
        self.corps_g = ", ".join((sql_ent_g))
        self.g_complete = self.entete_g+"id INTEGER PRIMARY KEY, time_left REAL, "+self.corps_g+")"

        # Table 3 computed weights article ean
        self.w_entete = "CREATE TABLE IF NOT EXISTS in_weight ("
        self.w_corps = ", ".join((sql_w_ent))
        self.w_complete = self.w_entete+"time_glob REAL PRIMARY KEY, "+self.w_corps+", total_art_topick INTEGER, total_ean_topick INTEGER)"
        
        # Table 4 computed speed article ean
        self.speedtheo_entete = "CREATE TABLE IF NOT EXISTS in_speed ("
        self.speedtheo_corps = ", ".join((sql_speed))
        self.speed_complete = self.speedtheo_entete + "id INTEGER PRIMARY KEY, "+self.speedtheo_corps+", speed_art_avg FLOAT, speed_ean_avg FLOAT)"

        # Table 5 computed delta article ean
        self.entete_delta = "CREATE TABLE IF NOT EXISTS delta_table ("
        self.corps_delta = ", ".join((sql_delta))
        self.delta_complete = self.entete_delta+"id INTEGER PRIMARY KEY, delta_time REAL, "+self.corps_delta+")"
        
        self.conn = sqlite3.connect(db)
        self.cur = self.conn.cursor()
        self.cur.execute(self.complete)
        self.cur.execute(self.g_complete)
        self.cur.execute(self.w_complete)
        self.cur.execute(self.speed_complete)
        self.cur.execute(self.delta_complete)

        # DO NOT DELETE : global list of art. ean used in backbone.add_arteanpik() 
        lsartean.insert(0, "time_glob")
        lsartean.insert(len(lsartean), "total_pickers")

    def createtotalpick(self, numofblock, db):
        global ls_total
        sql_total = []
        self.numoblock = numofblock

        ls_total = ["total_picked_artbck{}".format(nblock) for nblock in range(0, self.numofblock)] + ["total_picked_eanbck{}".format(nblock) for nblock in range(0, self.numofblock)] + ["totall_art", "totall_ean"]

        
        sql_total = helper_dbtype(ls_total, "INTEGER")
        
        # for artean_picked in ls_total:
        #     self.attrib_total = " ".join((artean_picked, "INTEGER"))
        #     sql_total.append(self.attrib_total)

        # Table 6 input total vol article ean picked
        self.begin = "CREATE TABLE IF NOT EXISTS total_out ("
        self.body = ", ".join((sql_total))
        self.completed = self.begin+"id INTEGER PRIMARY KEY, time_glob REAL, "+self.body+", FOREIGN KEY (time_glob) REFERENCES in_globalpick (time_glob))"
        self.conn = sqlite3.connect(db)
        self.cur = self.conn.cursor()
        self.cur.execute(self.completed)

    def insert_nameblock(self, block_id, name):
        self.cur.execute("INSERT INTO blocks_in VALUES (?,?)",(block_id, name))
        
        #self.cur.execute("CREATE TABLE IF NOT EXISTS tasks_in (id INTEGER PRIMARY KEY, task_id INTEGER, task_time FLOAT, FOREIGN KEY (task_id) REFERENCES blocks_in (block_id))") #id INTEGER PRIMARY KEY,
        # TO DELETE self.cur.execute("CREATE TABLE IF NOT EXISTS {}_task (id INTEGER PRIMARY KEY, picker text, task_time FLOAT, start_time REAL, end_time REAL)".format(name)) #id INTEGER PRIMARY KEY, 
        self.conn.commit()

    def __del__(self):
        self.conn.close()


"""
creates new tables on fly
"""
class CreateDB_OnFly:
    def __init__(self, db="./database/dispatch_data.db"):
        self.conn = sqlite3.connect(db)
        self.cur = self.conn.cursor()
        self.ini_pickers = False
        self.cur.execute("CREATE TABLE IF NOT EXISTS tasks_in (id INTEGER PRIMARY KEY, block_name text, task_time FLOAT)")
        self.cur.execute("CREATE TABLE IF NOT EXISTS pickers (id INTEGER PRIMARY KEY, name text NOT NULL, arrival_time REAL, stock_of_time FLOAT)")
        self.conn.commit()
    
    # Table x pickers
    def insert_pickers(self, id, picker_name, arrival_time, stock_of_time):
    
        #for npicker in range(num_picker):
            #self.cur.execute("INSERT INTO blocks_in VALUES (?,?)",(id, "Picker_{}".format(npicker)))
        self.cur.execute("INSERT INTO pickers VALUES (?,?,?,?)",(id, picker_name, arrival_time, stock_of_time))
        self.conn.commit()

    # task table insertion
    def insert_tasks(self, task_time, blockname):
        values = [(task_value, task_name) for task_value, task_name in zip(task_time,  blockname)]
       
        print(values)
            #self.cur.executemany("INSERT INTO tasks_in (task_id, task_time) VALUES ((SELECT block_id FROM blocks_in WHERE name=?),?)", values)
        self.cur.executemany("INSERT INTO tasks_in (task_time, block_name) VALUES (?,?)", list(values))
        self.conn.commit()

    def __del__(self):
        self.conn.close()

class UsingDB:
    def __init__(self, db="./database/input_data.db"):
        self.conn = sqlite3.connect(db)
        self.cur = self.conn.cursor()

    def fetch_hourout(self):
        self.cur.execute("SELECT time_glob FROM in_globalpick ORDER BY time_glob DESC LIMIT 1")
        rows = self.cur.fetchall()

        return rows

    def fetch_art_ean_input(self):
        self.cur.execute("SELECT * FROM in_globalpick ORDER BY time_glob DESC LIMIT 1")
        rows = self.cur.fetchall()

        return rows

    def fetch_picker(self, block_id):
        self.cur.execute("SELECT num_picker FROM block_picker_out WHERE block_id=?",(block_id,))
        rows = self.cur.fetchall()

        return rows

    def fetch_total_picker(self):
        self.cur.execute("SELECT total_picker FROM block_picker_out ORDER BY total_picker DESC LIMIT 1")
        rows = self.cur.fetchall()

        return rows

    """
    @param self: nothing
    @return row: goal of art
    """
    def fetch_artgoal(self):
          
        self.middle = len(ls_goal_g) // 2
        self.artcolumn = ', '.join(ls_goal_g[ : self.middle])
        self.sqlagoal = "SELECT %s FROM %s ORDER BY id" % (self.artcolumn, 'goalpick')
        self.cur.execute(self.sqlagoal)
        row = self.cur.fetchone()

        return row

    """
    @param self: nothing
    @return row: goal of ean
    """
    def fetch_eangoal(self):

        self.middle = len(ls_goal_g) // 2
        self.eancolumn = ', '.join(ls_goal_g[self.middle: ])
        self.sqlegoal = "SELECT %s FROM %s ORDER BY id" % (self.eancolumn, 'goalpick')
        self.cur.execute(self.sqlegoal)
        row = self.cur.fetchone()

        return row

    def insert_dicsql(self, dictbase, str_table_name):
        self.dictbase = dictbase
        self.placeholder = ','.join(['?'] * len(self.dictbase))
        self.column = ', '.join(self.dictbase.keys())
        

        self.sql = "INSERT INTO %s (%s) VALUES (%s)" % (str_table_name, self.column, self.placeholder)
        self.cur.execute(self.sql, list(self.dictbase.values()))
        self.conn.commit()


    def compute_totals(self):
        back_uplist = []
        self.sumart = 0
        self.sumean = 0
        self.cur.execute("SELECT * FROM total_out")
        self.totcol = [description[0] for description in self.cur.description]

        self.totalcolumn = ', '.join(self.totcol[1:])
        self.questmark = ','.join(['?'] * (len(self.totcol)-1))

        self.timeglob = "SELECT time_glob FROM in_globalpick ORDER BY time_glob DESC LIMIT 1"
        self.cur.execute(self.timeglob)
        back_uplist.append(self.cur.fetchone()[0])

        for ddelta, dtotal in zip(ls_delta, self.totcol[1:-2]):
            self.sqltotal = "SELECT SUM(%s) as %s FROM %s" % (ddelta, dtotal, 'delta_table')
            self.cur.execute(self.sqltotal)
            back_uplist.append(abs(self.cur.fetchone()[0]))

        self.middleblock = (len(back_uplist)-1) // 2

        for x in range(self.middleblock):
            self.sumart += back_uplist[x+1]
            self.sumean += back_uplist[x+1+self.middleblock]

        back_uplist.append(self.sumart)
        back_uplist.append(self.sumean)

        self.sqltotal = "INSERT INTO total_out (%s) VALUES (%s)" % (self.totalcolumn, self.questmark)
        self.cur.execute(self.sqltotal, back_uplist)
        self.conn.commit()

    """
    def remove(self, blocks_in):
        self.cur.execute("DELETE FROM blocks_in WHERE blocks_in=?", (blocks_in))
        self.conn.commit()
    
    def update(self, article, ean, picker):
        self.cur.execute("UPDATE blocks_in SET article = ?, ean = ?, picker = ?",
        (article, ean, picker))
        self.conn.commit()
    """

    def __del__(self):
        self.conn.close()