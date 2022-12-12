import pandas as pd
import numpy as np
import sqlite3
import globaldb
from globaldb import UsingDB
import adminblocks

globaldf = pd.DataFrame() # dataframe of input art and ean

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

        self.df = pd.read_sql_query("select * from in_globalpick", self.conn)
        print(self.df.head())
        #self.conn.close()


class Computing:
    def __init__(self, db):

        try:
            self.conn = sqlite3.connect(db)
            self.cur = self.conn.cursor()
        except Exception as e:
            print(f'An error occurred: {e}.')
            exit()

    def weightnratio(self, dictbase):
        """This function computes the weights of articles, eans and ration article/ean"""

        global globaldf # dataframe of input article, ean data
        
        # get the data from entry sql table
        self.dictbase = dictbase
        self.sql_query = pd.read_sql_query("SELECT * FROM in_globalpick ORDER BY time_glob DESC LIMIT 1", self.conn)

        globaldf = pd.DataFrame(self.sql_query, columns=[key for key in dictbase.keys()])
        
        # doing some maths to get total, weight

        self.dfwr = globaldf.drop(columns=['total_pickers'], axis=1)

        self.middle = len(self.dfwr.columns) //2 # getting the frontier between art and ean
        self.lencolbase = len(self.dfwr.columns) 
        self.dfwr['total_art_topick'], self.dfwr['total_ean_topick'] = self.dfwr.iloc[:, 1 : self.middle+1].sum(axis=1), self.dfwr.iloc[:, self.middle+1 : self.lencolbase].sum(axis=1)

        self.countblocks = len(self.dfwr.columns[1:self.middle+1])
    
        for self.block in range(0, self.countblocks):
            self.dfwr["wartbck{}".format(self.block)] = self.dfwr["artbck{}".format(self.block)] / self.dfwr['total_art_topick']
        for self.block in range(0, self.countblocks):
            self.dfwr["weanbck{}".format(self.block)] = self.dfwr["eanbck{}".format(self.block)] / self.dfwr['total_ean_topick']
        for self.block in range(0, self.countblocks):
            self.dfwr["ratioaebck{}".format(self.block)] = self.dfwr["artbck{}".format(self.block)] / self.dfwr["eanbck{}".format(self.block)]

            self.dfwr = self.dfwr.drop(["artbck{}".format(self.block), "eanbck{}".format(self.block)], axis = 1)

        # reordering the column to fit to the sql 'in_weight_globpick' table order 
        self.temp_col = self.dfwr.columns.tolist()
        self.new_col = self.temp_col[:1] + self.temp_col[3:] + self.temp_col[1:3]

        self.newdfwr = self.dfwr[self.new_col]

        # gathering the string and data
        self.placeholdwr = ','.join(['?'] * len(self.newdfwr.columns))
        self.columnwr = ','.join(self.newdfwr.columns)

        self.sqlwr = "INSERT INTO in_weight_globpick VALUES (%s)" % (self.placeholdwr)

        self.mylist = list(self.newdfwr.iloc[-1][x] for x in self.newdfwr.columns)

        # important: convert np array int64 type to plain int
        self.mylist[-2], self.mylist[-1] = np.uint32(self.mylist[-2]).item(), np.uint32(self.mylist[-1]).item()
        self.mytuple = tuple(self.mylist)

        # nuture the sql 'in_weight_globpick' table
        self.cur.execute(self.sqlwr, self.mytuple)
        self.conn.commit()

    def goal(self, dictbase): # SET THE INITIAL GOAL / NEEDS ANOTHER FUNCTION FOR NEXT T >= 1 GOAl
        self.delta_prod()

        goaldb = UsingDB("./database/goatdata.db") # To Simplify if necessary
        self.goalkey = globaldb.ls_goal_g # list of futur keys' dict

        self.dictbase = dictbase

        self.time = self.dictbase.pop('time_glob')
        self.dictbase.pop('total_pickers')

        self.sql_weight = pd.read_sql_query("SELECT * FROM in_weight_globpick ORDER BY time_glob DESC LIMIT 1", self.conn)
        self.dfweight = pd.DataFrame(self.sql_weight) #, columns=[key for key in dictbase.keys()]
        
        self.cur.execute("SELECT count(*) FROM goalpick")
        
        if self.cur.fetchone() < 1:

            if adminblocks.setthegoal[0] > 0:
                self.weigthvol = adminblocks.setthegoal[0] / np.uint32(self.dfweight['total_art_topick']).item()
                self.dictgoal = dict(zip(self.goalkey,  list(self.weigthvol * vals for vals in self.dictbase.values())))
                self.dictgoal['time_glob'] = self.time
                goaldb.insert_goal(self.dictgoal)
                return self.dictgoal.items()

            elif adminblocks.setthegoal[1] > 0:  # RECORD THE 1ST AS BASED, THEN THE FOLLOWING IS THE DIFF WITH THE PREFIOUS LINE 1ST
                self.percent = adminblocks.setthegoal[1] / 100
                self.dictgoal = dict(zip(self.goalkey, list(self.percent * val for val in self.dictbase.values())))
                self.dictgoal['time_glob'] = self.time
                goaldb.insert_goal(self.dictgoal)
                return self.dictgoal

            else:
                self.dictgoal = dict(zip(self.goalkey, self.dictbase.values()))
                self.dictgoal['time_glob'] = self.time
                goaldb.insert_goal(self.dictgoal)
                return self.dictgoal
        
    def delta_prod(self):
        goaldb = UsingDB("./database/goatdata.db")
        self.sql_query = pd.read_sql_query("SELECT * FROM in_globalpick", self.conn)

        self.veryglobal = pd.DataFrame(self.sql_query)
        self.dfbase = self.veryglobal.drop(columns=['total_pickers'], axis=1)

        self.dfbase['time_glob'] = pd.to_datetime(self.dfbase['time_glob'])
        self.lsdelta_col = list(self.dfbase.columns)

        if len(self.dfbase) > 1:
            goaldb.insert_delta(self.dfbase.diff(axis=0))

class Dispatch():

    def __init__(self):
        pass

    """
    TOTAL CAPACITIF
    Total picker * capacitif goal/h * number of hours

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

        