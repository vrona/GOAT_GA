import pandas as pd
import sqlite3

#import pandas as pd
capatheodictfull = {}

class Engine():

    def __init__(self): #, db

    #     self.conn = sqlite3.connect(db)
    #     self.cur = self.conn.cursor()
        pass
        

    #def sumit(self, dictofnum):
    #def subit(self, goal, real):

    #def trendit(self, ):

    #def delta_time(self, starting_time, ending_time):

    # def weights(self, dictofnum):

    def querygb_inputs(self):
        #self.conn = 

        self.df = pd.read_sql_query("select * from in_globalpick", self.conn)
        print(self.df.head())
        self.conn.close()

class Computing:
    def __init__(self, db):
        self.conn = sqlite3.connect(db)
        self.cur = self.conn.cursor()

    def weightnratio(self, dictbase):
        #pdb = UsingDB("./database/goatdata.db")
        #self.anydict = anydict
        self.dictbase = dictbase
        self.sql_query = pd.read_sql_query("SELECT * FROM in_globalpick ORDER BY time_glob DESC LIMIT 1", self.conn)
        self.df = pd.DataFrame(self.sql_query, columns=[key for key in dictbase.keys()])
        print(self.df)


    def insert_capatheo(self, dictcapat):
        self.dictcapat = dictcapat
        self.placeholder = ','.join(['?'] * len(self.dictcapat))
        self.column = ', '.join(self.dictcapat.keys())
        self.sql = "INSERT INTO %s (%s) VALUES (%s)" % ('in_capatheo', self.column, self.placeholder)
        
        self.cur.execute(self.sql, list(self.dictcapat.values()))
        self.conn.commit()

class Dispatch():

    def __init__(self):
        pass

    """
    TOTAL TO PICK
    - Sum Function:
    Sum of articles to pick
    Sum of ean to pick

    TOTAL CAPACITIF
    Total picker * capacitif goal/h * number of hours

    TOTAL PICKED
    Sum of articles picked up
    Sum of ean picked up

    WEIGHTS DISTRIBUTION
    Block real art / total articles to pick
    Block real ean / total ean to pick

    PICKERS DISTRIBUTION
    Total Picker * Ean weights
    Total Picker * Articles weights

    TRENDING
    - Trend pick/hour
    - Trend pick/all_passed_hours
    Forecast Picking next hour and shift  -> y = ax + b
    
    DELTA CAPACITIF
    capacitif goal/h - real capacitif picked/h
    Forecast : total capacitif - Trend pick/all_passed_hours
   
    POLY FUNCTION
    delta time = time ending shift - time of record
    """

        