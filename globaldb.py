import sqlite3

class ProdDB:
    def __init__(self, db) :
        self.dictbase = {}
        self.conn = sqlite3.connect(db)
        self.cur = self.conn.cursor()
        self.cur.execute("CREATE TABLE IF NOT EXISTS blocks_in (id INTEGER PRIMARY KEY, name text NOT NULL)")
        self.cur.execute("CREATE TABLE IF NOT EXISTS globalpick_in (time_glob REAL PRIMARY KEY, art_bck1 INTEGER,art_bck2 INTEGER,art_bck3 INTEGER,art_bck4 INTEGER,art_bck5 INTEGER,art_bck6 INTEGER,ean_bck1 INTEGER,ean_bck2 INTEGER,ean_bck3 INTEGER,ean_bck4 INTEGER,ean_bck5 INTEGER,ean_bck6 INTEGER,total_pickers INTEGER NOT NULL)")
        self.cur.execute("CREATE TABLE IF NOT EXISTS capa (capatheo_h REAL NOT NULL)")
        self.cur.execute("CREATE TABLE IF NOT EXISTS totals_out (id INTEGER PRIMARY KEY, timeofrecord REAL NOT NULL, total_prelev INTEGER NOT NULL, delta_capacitif INTEGER NOT NULL, total_predic INTEGER NOT NULL, capareal_h INTEGER NOT NULL, capaavg INTEGER, FOREIGN KEY (timeofrecord) REFERENCES globalpick_in (time_glob))")
        self.cur.execute("CREATE TABLE IF NOT EXISTS block_picker_out (block_id PRIMARY KEY, num_picker INTEGER, total_picker INTEGER, FOREIGN KEY (block_id) REFERENCES blocks_in (id), FOREIGN KEY (total_picker) REFERENCES globalpick_in (total_pickers))")
        self.cur.execute("CREATE TABLE IF NOT EXISTS pickers_out (id INTEGER PRIMARY KEY, name VARCHAR NOT NULL, time_block_arrival record REAL NOT NULL, time_block_departure REAL NOT NULL, block_id_origin INTEGER, block_id_landing INTEGER, FOREIGN KEY (block_id_origin) REFERENCES blocks_in (id))")
        self.cur.execute("CREATE TABLE IF NOT EXISTS poly_out (time_glob REAL PRIMARY KEY, total_picker_onsite INTEGER NOT NULL, total_pick_goal INTEGER NOT NULL, poly_status INTEGER, FOREIGN KEY (total_picker_onsite) REFERENCES globalpick_in (time_glob), FOREIGN KEY (time_glob) REFERENCES globalpick_in (total_pickers))")
        self.conn.commit()

    def fetch_hourout(self) :
        self.cur.execute("SELECT time_glob FROM globalpick_in ORDER BY time_glob DESC LIMIT 1")
        rows = self.cur.fetchall()
        return rows

    def fetch_picker(self, block_id) :
        self.cur.execute("SELECT num_picker FROM block_picker_out WHERE block_id=?",(block_id,))
        rows = self.cur.fetchall()
        return rows

    def fetch_total_picker(self) :
        self.cur.execute("SELECT total_picker FROM block_picker_out ORDER BY total_picker DESC LIMIT 1")
        rows = self.cur.fetchall()
        return rows

    def insert_capatheo(self, capatheo_h):
        self.cur.execute("INSERT INTO capa VALUES (?)",(capatheo_h,))
        self.conn.commit()

    def insert_nameblock(self, id, name):
        self.cur.execute("INSERT INTO blocks_in VALUES (?,?)",(id, name))
        self.conn.commit()
    
    def insert_poly(self, time_glob, total_picker_onsite):
        self.cur.execute("INSERT INTO poly_out VALUES (?,?)",(time_glob, total_picker_onsite))
        self.conn.commit()

    def insert_gpick(self, dictbase):
        self.dictbase = dictbase
        self.placeholder = ','.join(['?'] * len(self.dictbase))
        self.column = ', '.join(self.dictbase.keys())
        self.sql = "INSERT INTO %s (%s) VALUES (%s)" % ('globalpick_in', self.column, self.placeholder)
        
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