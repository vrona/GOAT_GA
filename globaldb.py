import sqlite3
import pandas as pd

lsartean = []
ls_w_artean = []

class CreationDB:
    def __init__(self, numofblock, db):
        self.dictbase = {}
        self.numofblock = numofblock
        self.conn = sqlite3.connect(db)
        self.cur = self.conn.cursor()
        self.createglobalpick(self.numofblock, db)
        self.cur.execute("CREATE TABLE IF NOT EXISTS blocks_in (id INTEGER PRIMARY KEY, name text NOT NULL)")
        self.cur.execute("CREATE TABLE IF NOT EXISTS capa (capatheo_h REAL NOT NULL)")
        self.cur.execute("CREATE TABLE IF NOT EXISTS totals_out (id INTEGER PRIMARY KEY, timeofrecord REAL NOT NULL, total_prelev INTEGER NOT NULL, delta_capacitif INTEGER NOT NULL, total_predic INTEGER NOT NULL, capareal_h INTEGER NOT NULL, capaavg INTEGER, FOREIGN KEY (timeofrecord) REFERENCES in_globalpick (time_glob))")
        self.cur.execute("CREATE TABLE IF NOT EXISTS block_picker_out (block_id PRIMARY KEY, num_picker INTEGER, total_picker INTEGER, FOREIGN KEY (block_id) REFERENCES blocks_in (id), FOREIGN KEY (total_picker) REFERENCES in_globalpick (total_pickers))")
        self.cur.execute("CREATE TABLE IF NOT EXISTS pickers_out (id INTEGER PRIMARY KEY, name VARCHAR NOT NULL, time_block_arrival record REAL NOT NULL, time_block_departure REAL NOT NULL, block_id_origin INTEGER, block_id_landing INTEGER, FOREIGN KEY (block_id_origin) REFERENCES blocks_in (id))")
        self.cur.execute("CREATE TABLE IF NOT EXISTS poly_out (time_glob REAL PRIMARY KEY, total_picker_onsite INTEGER NOT NULL, total_pick_goal INTEGER NOT NULL, poly_status INTEGER, FOREIGN KEY (total_picker_onsite) REFERENCES in_globalpick (time_glob), FOREIGN KEY (time_glob) REFERENCES in_globalpick (total_pickers))")
        self.conn.commit()

    def createglobalpick(self, numofblock, db):
        global lsartean
        sql_ent = []
        sql_w_ent = []
        self.numoblock = numofblock
        
        lsartean = ["artbck{}".format(nblock) for nblock in range(0, self.numofblock)] + ["eanbck{}".format(nblock) for nblock in range(0, self.numofblock)]
        ls_w_artean = ["wartbck{}".format(nblock) for nblock in range(0, self.numofblock)] + ["weanbck{}".format(nblock) for nblock in range(0, self.numofblock)]

        for artean in lsartean:
            self.attribute = ' '.join((artean, "INTEGER"))
            sql_ent.append(self.attribute)
        
        for w_artean in lsartean:
            self.w_attribute = ' '.join((w_artean, "FLOAT"))
            sql_w_ent.append(self.w_attribute)

        self.entete = "CREATE TABLE IF NOT EXISTS in_globalpick ("
        self.corps = ', '.join((sql_ent))
        self.complete = self.entete + "time_glob REAL PRIMARY KEY" + ", " + self.corps + ", total_pickers INTEGER NOT NULL)"

        self.w_entete = "CREATE TABLE IF NOT EXISTS in_weight_globpick ("
        self.w_corps = ', '.join((sql_w_ent))
        self.w_complete = self.w_entete + "time_glob REAL PRIMARY KEY" + ", " + self.w_corps + ", total_art_topick INTEGER, total_ean_topick INTEGER)"
        
        self.conn = sqlite3.connect(db)
        self.cur = self.conn.cursor()
        self.cur.execute(self.complete)
        self.cur.execute(self.w_complete)
        
        lsartean.insert(0, "time_glob")
        lsartean.insert(len(lsartean), "total_pickers")

    def insert_nameblock(self, id, name):
        self.cur.execute("INSERT INTO blocks_in VALUES (?,?)",(id, name))
        self.conn.commit()

class UsingDB:
    def __init__(self, db):
        self.conn = sqlite3.connect(db)
        self.cur = self.conn.cursor()

    def fetch_hourout(self):
        self.cur.execute("SELECT time_glob FROM in_globalpick ORDER BY time_glob DESC LIMIT 1")
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

    def insert_capatheo(self, capatheo_h):
        self.cur.execute("INSERT INTO capa VALUES (?)",(capatheo_h,))
        self.conn.commit()

    def insert_poly(self, time_glob, total_picker_onsite):
        self.cur.execute("INSERT INTO poly_out VALUES (?,?)",(time_glob, total_picker_onsite))
        self.conn.commit()

    def insert_gpick(self, dictbase):
        self.dictbase = dictbase
        self.placeholder = ','.join(['?'] * len(self.dictbase))
        self.column = ', '.join(self.dictbase.keys())
        self.sql = "INSERT INTO %s (%s) VALUES (%s)" % ('in_globalpick', self.column, self.placeholder)
        
        self.cur.execute(self.sql, list(self.dictbase.values()))
        self.conn.commit()

    def insert_totals_out(self, id, timeofrecord, total_prelev, delta_capacitif, total_predic, capareal_h, capaavg):
        self.cur.execute("INSERT INTO totals_out VALUES (?,?,?,?,?,?,?)",(id, timeofrecord, total_prelev, delta_capacitif, total_predic, capareal_h, capaavg))
        self.conn.commit()

    def insert_block_picker_out(self, id, timeofrecord, block_id_origin, block_id_landing, picker):
        self.cur.execute("INSERT INTO block_picker_out VALUES (?,?,?,?,?)",(id, timeofrecord, block_id_origin, block_id_landing, picker))
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

# db = ProdDB('globaldata.db')
# dictglob = {}

# def auto(list1, list2):
#     for k, v in zip(list1, list2):
#         dictglob[k]= v
#     #print(dictglob)

# dval = [datetime.datetime.now(),12000,13000,14000,15000,16000,17000,2000,3000,4000,5000,6000,7000,10]
# dkey = ['time_glob', 'art_bck1', 'art_bck2', 'art_bck3', 'art_bck4', 'art_bck5', 'art_bck6', 'ean_bck1', 'ean_bck2', 'ean_bck3', 'ean_bck4', 'ean_bck5', 'ean_bck6', 'total_pickers']

# auto(dkey, dval)

# db.insert_gpick(dictglob)
# db.insert_nameblock(0, "SportCo")
# db.insert_nameblock(1, "Chasse")
# db.insert_nameblock(2, "Glisse")
# db.insert_nameblock(3, "Running")
# db.insert_nameblock(4, "Implant")
# db.insert_nameblock(5, "PFECA")
# db.insert_capatheo(238.3)

#print(db.fetch_picker(1))