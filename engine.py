import pandas as pd
import sqlite3
import globaldb

globaldf = pd.DataFrame()

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
    def __init__(self, db, ):
        
        self.conn = sqlite3.connect(db)
        self.cur = self.conn.cursor()

    def weightnratio(self, dictbase):
        global globaldf
        # get the data from entry data
        self.dictbase = dictbase
        self.sql_query = pd.read_sql_query("SELECT * FROM in_globalpick ORDER BY time_glob DESC LIMIT 1", self.conn)
        globaldf = pd.DataFrame(self.sql_query, columns=[key for key in dictbase.keys()])

        # doing some maths to get total, weight
        self.dfwr = globaldf.drop(columns='total_pickers')
        self.middle = len(self.dfwr.columns) //2 # getting the frontier between art and ean
        self.lencolbase = len(self.dfwr.columns) 
        self.dfwr['total_art_topick'], self.dfwr['total_ean_topick'] = [self.dfwr.iloc[:, 1 : self.middle+1].sum(axis=1), self.dfwr.iloc[:, self.middle+1 : self.lencolbase].sum(axis=1)]
        
        self.countblocks = len(self.dfwr.columns[1:self.middle+1])
    
        for self.block in range(0, self.countblocks):
            self.dfwr["wartbck{}".format(self.block)] = self.dfwr["artbck{}".format(self.block)] / self.dfwr['total_art_topick']
        for self.block in range(0, self.countblocks):
            self.dfwr["weanbck{}".format(self.block)] = self.dfwr["eanbck{}".format(self.block)] / self.dfwr['total_ean_topick']
        for self.block in range(0, self.countblocks):
            self.dfwr["ratioaebck{}".format(self.block)] = self.dfwr["artbck{}".format(self.block)] / self.dfwr["eanbck{}".format(self.block)]

            self.dfwr = self.dfwr.drop(["artbck{}".format(self.block), "eanbck{}".format(self.block)], axis = 1)

        # reordering the column to fit to the sql table order in_weight_globpick
        self.temp_col = self.dfwr.columns.tolist()
        self.new_col = self.temp_col[:1] + self.temp_col[3:] + self.temp_col[1:3]
        self.dfwr = self.dfwr[self.new_col]

        self.placeholdwr = ','.join(['?'] * len(self.dfwr.columns))
        self.columnwr = ','.join(self.dfwr.keys())
        print(self.dfwr)
        print(self.placeholdwr, '\n',self.columnwr)

        self.sqlwr = "INSERT INTO %s (%s) VALUES (%s)" % ('in_weight_globpick', self.columnwr, self.placeholdwr)
        print(self.sqlwr)

        #PROBLEM PROBLEM PROBLEM
        self.cur.execute(self.sqlwr, list(self.dfwr.iloc[-1][x] for x in self.dfwr.keys()))
        self.conn.commit()


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

        