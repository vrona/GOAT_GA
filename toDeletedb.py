"""import sqlite3

class Database:
    def __init__(self, db) :
        self.conn = sqlite3.connect(db)
        self.cur = self.conn.cursor()
        self.cur.execute("CREATE TABLE IF NOT EXISTS teamdb (article int, ean int, dkt_pickers int)") #cumul_pick int, avg_prod_picker int
        self.conn.commit()
    
    def fetch(self) :
        self.cur.execute("SELECT * FROM teamdb")
        rows = self.cur.fetchall()
        return rows

    def insertart(self, articles): #, cumul_pick, avg_prod_picker):
        self.cur.execute("INSERT INTO teamdb VALUES (?)",(articles))
        self.conn.commit()

    def insertean(self, ean): #, cumul_pick, avg_prod_picker):
        self.cur.execute("INSERT INTO teamdb VALUES (?)",(ean))
        self.conn.commit()

    def remove(self, blocks):
        self.cur.execute("DELETE FROM teamdb WHERE blocks=?", (blocks,))
        self.conn.commit()
    
    def update(self, articles, ean, dkt_pickers):
        self.cur.execute("UPDATE teamdb SET articles = ?, ean = ?, dkt_pickers = ?",
        (articles, ean, dkt_pickers))
        self.conn.commit()

    def __del__(self):
        self.conn.close()

db = Database('store.db')
db.insertart(42000)
db.insertean(19363996)
#db.insert("1490", "3712", "5834")"""