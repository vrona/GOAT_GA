import sqlite3
import datetime

class PickingDB:
    def __init__(self, db) :
        self.conn = sqlite3.connect(db)
        self.cur = self.conn.cursor()
        self.cur.execute("CREATE TABLE IF NOT EXISTS blocks (id integer PRIMARY KEY, name text NOT NULL)")
        self.cur.execute("CREATE TABLE IF NOT EXISTS pickingrecord (id integer PRIMARY KEY,timeofrecord real NOT NULL, article integer NOT NULL, ean integer NOT NULL, picker integer NOT NULL, block_id integer NOT NULL, FOREIGN KEY (block_id) REFERENCES blocks (id))")
        self.cur.execute("CREATE TABLE IF NOT EXISTS fixdata (id integer PRIMARY KEY, totalpicker integer NOT NULL, capaheure integer NOT NULL)")
        self.conn.commit()
    
    def fetch_picker(self, block_id) :
        self.cur.execute("SELECT picker FROM pickingrecord WHERE block_id=?",(block_id,))
        rows = self.cur.fetchall()
        return rows

    def fetch_hour(self) :
        self.cur.execute("SELECT timeofrecord FROM pickingrecord WHERE block_id=1")
        rows = self.cur.fetchall()
        return rows

    def insert_nameblock(self, id, name):
        self.cur.execute("INSERT INTO blocks VALUES (?,?)",(id, name))
        self.conn.commit()

    def insert_bckdata(self, id, timeofrecord, article, ean, picker, block_id):
        self.cur.execute("INSERT INTO pickingrecord VALUES (?,?,?,?,?,?)",(id, timeofrecord, article, ean, picker, block_id))
        self.conn.commit()

    def insert_fixdata(self, totalpicker, capaheure):
        self.cur.execute("INSERT INTO fixdata VALUES (NULL,?,?)",(totalpicker, capaheure,))
        self.conn.commit()

    def insert_one(self, article):
        self.cur.execute("INSERT INTO pickingrecord VALUES (?)",(article))
        self.conn.commit()

    def update_one(self, article):
        self.cur.execute("UPDATE pickingrecord SET article =? WHERE id = ?",(article))
        self.conn.commit()

    """
    def remove(self, blocks):
        self.cur.execute("DELETE FROM blocks WHERE blocks=?", (blocks))
        self.conn.commit()
    
    def update(self, article, ean, picker):
        self.cur.execute("UPDATE blocks SET article = ?, ean = ?, picker = ?",
        (article, ean, picker))
        self.conn.commit()
    """

    def __del__(self):
        self.conn.close()

#db = PickingDB('localstorage.db')
#print(db.fetch_picker(1))
# db.insert_nameblock(1, "SportCo")
# db.insert_nameblock(2, "Chasse")
# db.insert_nameblock(3, "Glisse")
# db.insert_nameblock(4, "Running")
# db.insert_nameblock(5, "Implant")
# db.insert_bckdata(1, datetime.datetime.now(), 2922, 1936, 2, 1)
# db.insert_bckdata(2, datetime.datetime.now(), 3996, 1990, 2, 2)
# db.insert_bckdata(3, datetime.datetime.now(), 3912, 3064, 3, 3)
# db.insert_bckdata(4, datetime.datetime.now(), 5864, 3780, 4, 4)
# db.insert_bckdata(5, datetime.datetime.now(), 0, 0, 0, 5)
#db.insert_fixdata(11, 234.2)
#db.update_one(200)