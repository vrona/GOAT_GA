import sqlite3

lsartean = []
ls_goal_g = []
ls_w_artean = []
ls_speed_artean = []
ls_delta = []
ls_total = []
ls_task_data = []
prev_dicttask = {}

# helper func for sql tables creation: joins column_name datatype
def helper_dbtype(listofsth, datatype):
    listofall = []

    for column_name in listofsth:
        attribute = " ".join((column_name, datatype))
        listofall.append(attribute)
    return listofall


class CreationDB:
    """
    class dedicated to table that records picking figures of any kind. Produces a 1st .db file: input_data
    """
    def __init__(self, numofblock, db="./database/input_data.db"):
        self.dictbase = {}
        self.numofblock = numofblock
        self.conn = sqlite3.connect(db)
        self.cur = self.conn.cursor()
        self.createglobalpick(self.numofblock, db)
        # Table 6 input blocks' id and name open for picking
        self.cur.execute("CREATE TABLE IF NOT EXISTS blocks_in (block_id INTEGER PRIMARY KEY, block_name text NOT NULL)")
        
        self.createtotalpick(self.numofblock, db)
        
        self.conn.commit()

    def createglobalpick(self, numofblock, db):
        """
        creates multi dynamic tables. Columns' names and numbers are based on the number of blocks opened at the beginning of the shift.
        """
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
        """
        creates a unique dynamic table. Columns' names and numbers are based on the number of blocks opened at the beginning of the shift.
        """
        global ls_total
        sql_total = []
        self.numoblock = numofblock

        ls_total = ["total_picked_artbck{}".format(nblock) for nblock in range(0, self.numofblock)] + ["total_picked_eanbck{}".format(nblock) for nblock in range(0, self.numofblock)] + ["totall_art", "totall_ean"]

        sql_total = helper_dbtype(ls_total, "INTEGER")

        # Table 7 input total vol article ean picked
        self.begin = "CREATE TABLE IF NOT EXISTS total_out ("
        self.body = ", ".join((sql_total))
        self.completed = self.begin+"id INTEGER PRIMARY KEY, time_glob REAL, "+self.body+", FOREIGN KEY (time_glob) REFERENCES in_globalpick (time_glob))"
        self.conn = sqlite3.connect(db)
        self.cur = self.conn.cursor()
        self.cur.execute(self.completed)

    # insertion of #blocks' id and name open for picking
    def insert_nameblock(self, block_id, block_name):
        self.cur.execute("INSERT INTO blocks_in VALUES (?,?)",(block_id, block_name))
        self.conn.commit()

    def __del__(self):
        self.conn.close()



class CreateDB_OnFly:
    """
    class dedicated to table that records dispatch of task (from each block) among picker. Produces a 2nd .db file: dispatch_data
    """
    def __init__(self, db="./database/dispatch_data.db"):
        self.conn = sqlite3.connect(db)
        self.cur = self.conn.cursor()
        self.ini_pickers = False
        self.ini_task_w_picker = False
        # Table +10 tasks_in recording total task per block
        self.cur.execute("CREATE TABLE IF NOT EXISTS tasks_in (id INTEGER PRIMARY KEY, block_name text, task_time FLOAT)")
        
        self.conn.commit()


    def create_pickers(self, numofblock, db):
        """
        creates unique dynamic table. Columns' names and numbers are based on the number of blocks opened at the beginning of the shift.
        """
        self.numofblock = numofblock
        ls_task_name = ["task_name{}".format(nblock) for nblock in range(0, self.numofblock)]
        ls_task_value = ["task_value{}".format(nblock) for nblock in range(0, self.numofblock)]
        ls_time_ending = ["time_ending{}".format(nblock) for nblock in range(0, self.numofblock)]
        
        sql_tn = helper_dbtype(ls_task_name, "text")
        sql_tv = helper_dbtype(ls_task_value, "FLOAT")
        sql_te = helper_dbtype(ls_time_ending, "real")

        # Table 8 input and partly computed data into pickers table
        self.entete_picker = "CREATE TABLE IF NOT EXISTS pickers ("
        self.corps_tn = ", ".join((sql_tn))
        self.corps_tv = ", ".join((sql_tv))
        self.corps_te = ", ".join((sql_te))
        
        self.pick_comp = self.entete_picker+"id INTEGER PRIMARY KEY, name text NOT NULL, arrival_time REAL, stock_of_time FLOAT, "+self.corps_tn+", "+self.corps_tv+", "+self.corps_te+")"

        self.conn = sqlite3.connect(db)
        self.cur = self.conn.cursor()
        self.cur.execute(self.pick_comp)
        self.conn.commit()


    def create_table_tasks(self, block_name, listofpicker, db):
        """
        creates unique table per open block. Each picker receive an amount of task to do based on his/her available time.
        """
        # Table +9... for ex.: C_Chasse_task, ... for each opened block
        sql_picker_name = helper_dbtype(listofpicker, "FLOAT")

        task_table_name = "{}_task".format(block_name)
        self.entete_taskpicker = "CREATE TABLE IF NOT EXISTS %s (" % task_table_name
        self.corps_pickername = ", ".join((sql_picker_name))

        self.task_picker = self.entete_taskpicker+"id INTEGER PRIMARY KEY, "+self.corps_pickername+")"

        self.conn = sqlite3.connect(db)
        self.cur = self.conn.cursor()
        self.cur.execute(self.task_picker)
        self.conn.commit()


    def update_table_picker_tasks(self, block_name, new_column_name):       
        """
        update column each "..._task" table  unique table per open block.
        Each picker receives an amount of task to do, based on his/her available time.
        """
        self.alter_task_picker = "ALTER TABLE %s_task ADD COLUMN %s FLOAT;" % (block_name, new_column_name)
        self.cur.execute(self.alter_task_picker)
        self.conn.commit()


    def insert_pickers(self, id, picker_name, arrival_time, stock_of_time):
        """
        insertion input data into pickers table
        """
        order = "INSERT INTO pickers (id,name,arrival_time,stock_of_time) VALUES (?,?,?,?)"
        param = list((id, picker_name, arrival_time, stock_of_time))
        self.cur.execute(order, param)
        self.conn.commit()


    def insert_tasks(self, task_time, blockname):
        """
        insertion computed task into tasks_in table
        """
        values = [(task_value, task_name) for task_value, task_name in zip(task_time,  blockname)]
        self.cur.executemany("INSERT INTO tasks_in (task_time, block_name) VALUES (?,?)", list(values))
        self.conn.commit()


    def insert_disp_taskpickr(self, block_name, listofdata):
        """
        insertion, into each "..._task" table, computed tasks distribution per picker
        """
        task_table_name = "{}_task".format(block_name)
        picker_name = []
        task_val = []
        
        # listofdata is basically the value (picker_name, task_times as tuple) of a dict.values()
        for t in listofdata:
            picker_name.append(t[0])
            task_val.append(t[1])
            # if t[1]:
            #     task_val.append(t[1])
            # else:
            #     task_val.append(0)

        placeholder = ','.join(['?'] * len(picker_name))
        column = ', '.join(picker_name)

        self.sql = "INSERT INTO %s (%s) VALUES (%s)" % (task_table_name, column, placeholder)
        self.cur.execute(self.sql, list(task_val))
        self.conn.commit()


    def __del__(self):
        self.conn.close()

class UsingDB:
    """
    class dedicated to use tables which contain recorded data mainly focused on the 1st .db file: input_data
    """
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
    
    def fetch_artgoal(self):
        """
        return row: goal of article per block
        """
        self.middle = len(ls_goal_g) // 2
        self.artcolumn = ', '.join(ls_goal_g[ : self.middle])
        self.sqlagoal = "SELECT %s FROM %s ORDER BY id" % (self.artcolumn, 'goalpick')
        self.cur.execute(self.sqlagoal)
        row = self.cur.fetchone()

        return row

    def fetch_eangoal(self):
        """
        return row: goal of ean per block
        """
        self.middle = len(ls_goal_g) // 2
        self.eancolumn = ', '.join(ls_goal_g[self.middle: ])
        self.sqlegoal = "SELECT %s FROM %s ORDER BY id" % (self.eancolumn, 'goalpick')
        self.cur.execute(self.sqlegoal)
        row = self.cur.fetchone()

        return row

    def insert_dicsql(self, dictbase, str_table_name):
        """
        helper func that inserts into str_table_name the content of the dictbase (keys are sql columns, values are sql rows)
        """
        self.dictbase = dictbase
        self.placeholder = ','.join(['?'] * len(self.dictbase))
        self.column = ', '.join(self.dictbase.keys())
        

        self.sql = "INSERT INTO %s (%s) VALUES (%s)" % (str_table_name, self.column, self.placeholder)
        self.cur.execute(self.sql, list(self.dictbase.values()))
        self.conn.commit()

    def compute_totals(self):
        """
        compute total picked (article, ean) per block
        """
        back_uplist = []
        self.sumart = 0
        self.sumean = 0
        self.cur.execute("SELECT * FROM total_out")

        # get column_name from total_out table to use for futur insertion
        self.totcol = [description[0] for description in self.cur.description]

        self.totalcolumn = ', '.join(self.totcol[1:])
        self.questmark = ','.join(['?'] * (len(self.totcol)-1))

        # get last data time from last input data recorded into in_globalpick table
        self.timeglob = "SELECT time_glob FROM in_globalpick ORDER BY time_glob DESC LIMIT 1"
        self.cur.execute(self.timeglob)
        back_uplist.append(self.cur.fetchone()[0])

        # compute total based on delta input data
        for ddelta, dtotal in zip(ls_delta, self.totcol[1:-2]):
            self.sqltotal = "SELECT SUM(%s) as %s FROM %s" % (ddelta, dtotal, 'delta_table')
            self.cur.execute(self.sqltotal)
            back_uplist.append(abs(self.cur.fetchone()[0]))

        # gathering data per article (1st half part of column) and ean (2nd half part)
        self.middleblock = (len(back_uplist)-1) // 2

        for x in range(self.middleblock):
            self.sumart += back_uplist[x+1]
            self.sumean += back_uplist[x+1+self.middleblock]

        back_uplist.append(self.sumart)
        back_uplist.append(self.sumean)

        # insertion into total_out table of computed total of article ean
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