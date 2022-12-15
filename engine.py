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

        # reordering the column to fit to the sql 'in_weight' table order 
        self.temp_col = self.dfwr.columns.tolist()
        self.new_col = self.temp_col[:1] + self.temp_col[3:] + self.temp_col[1:3]

        self.newdfwr = self.dfwr[self.new_col]

        # gathering the string and data
        self.placeholdwr = ','.join(['?'] * len(self.newdfwr.columns))
        self.columnwr = ','.join(self.newdfwr.columns)

        self.sqlwr = "INSERT INTO in_weight VALUES (%s)" % (self.placeholdwr)

        self.mylist = list(self.newdfwr.iloc[-1][x] for x in self.newdfwr.columns)

        # important: convert np array int64 type to plain int
        self.mylist[-2], self.mylist[-1] = np.uint32(self.mylist[-2]).item(), np.uint32(self.mylist[-1]).item()
        self.mytuple = tuple(self.mylist)

        # nuture the sql 'in_weight' table
        self.cur.execute(self.sqlwr, self.mytuple)
        self.conn.commit()

    def delta_prod(self):
            useofdb = UsingDB("./database/goatdata.db")
            self.sql_query = pd.read_sql_query("SELECT * FROM in_globalpick", self.conn)

            self.veryglobal = pd.DataFrame(self.sql_query)
            self.dfbase = self.veryglobal.drop(columns=['total_pickers'], axis=1)

            self.dfbase['time_glob'] = pd.to_datetime(self.dfbase['time_glob'])
            self.lsdelta_col = list(self.dfbase.columns)

            if len(self.dfbase) > 1:
                print(self.dfbase)
                useofdb.insert_delta(self.dfbase.diff(axis=0))

    def new_goal(self):
        self.delta_prod()

        useofdb = UsingDB("./database/goatdata.db") # To Simplify if necessary
        self.goalkey = globaldb.ls_goal_g # list of futur keys' dict

        self.sql_weight = pd.read_sql_query("SELECT * FROM in_weight ORDER BY time_glob DESC LIMIT 1", self.conn)
        self.dfweight = pd.DataFrame(self.sql_weight) #, columns=[key for key in dictbase.keys()]

        # check the length of goalpick table
        self.cur.execute("SELECT count(*) FROM goalpick")

        if self.cur.fetchone()[0] < 1:
             # query art, ean 1st inputs
            self.time = globaldf['time_glob'].values[-1]
            self.dfglobal = globaldf.drop(columns=['time_glob', 'total_pickers'], axis=1)

            if adminblocks.setthegoal[0] > 0:
                self.weigthvol = adminblocks.setthegoal[0] / np.uint32(self.dfweight['total_art_topick']).item()
                
                self.dictgoal = dict(zip(self.goalkey, list(self.weigthvol * self.dfglobal[col].values[-1] for col in self.dfglobal.columns)))
                self.dictgoal['time_glob'] = self.time
                useofdb.insert_dicsql(self.dictgoal, "goalpick")
                return self.dictgoal.items()

            elif adminblocks.setthegoal[1] > 0:
                self.percent = adminblocks.setthegoal[1] / 100
  
                self.dictgoal = dict(zip(self.goalkey,  list(self.percent * self.dfglobal[col].values[-1] for col in self.dfglobal.columns)))
                self.dictgoal['time_glob'] = self.time
                useofdb.insert_dicsql(self.dictgoal, "goalpick")
                return self.dictgoal

            else:
                self.dictgoal = dict(zip(self.goalkey, list(self.dfglobal[col].values[-1] for col in self.dfglobal.columns)))
                for k, v in self.dictgoal.items():
                    self.dictgoal[k] = int(v)
                self.dictgoal['time_glob'] = self.time
                useofdb.insert_dicsql(self.dictgoal, "goalpick")
                return self.dictgoal

        else:
            self.sql_goal = pd.read_sql_query("SELECT * FROM goalpick ORDER BY time_glob DESC LIMIT 1", self.conn)
            self.sql_input = pd.read_sql_query("SELECT * FROM in_globalpick ORDER BY time_glob DESC LIMIT 1", self.conn)
            self.dfnewgoal = self.sql_goal.drop(columns=['id','time_glob'], axis=1)

            self.sql_delta = pd.read_sql_query("SELECT * FROM delta_table ORDER BY delta_time DESC LIMIT 1", self.conn)
            self.sql_delta = self.sql_delta.drop(columns=['delta_time'], axis=1)

            self.newdictgoal = dict(zip(self.goalkey,  list(self.dfnewgoal.iloc[-1][colindex] + self.sql_delta.iloc[-1][colindex] for colindex in range(len(self.sql_delta.columns)))))

            # convert figures value as int
            for k, v in self.newdictgoal.items():
                self.newdictgoal[k] = int(v)
            self.newdictgoal['time_glob'] = self.sql_input['time_glob'].values[-1]
            
            useofdb.insert_dicsql(self.newdictgoal, "goalpick")

    def capacitif(self):
        self.dictspeed = {}
        self.df_ratio = self.weight()
        useofdb = UsingDB("./database/goatdata.db") # To Simplify if necessary
        self.df_delta = pd.read_sql_query("SELECT * FROM delta_table ORDER BY delta_time DESC LIMIT 1", self.conn)
        #self.df_delta = self.sql_delta.drop(columns=['id'], axis=1) # perhaps drop ''

        self.df_capa = pd.read_sql_query("SELECT * FROM in_capa", self.conn)
        # check the length of goalpick table
        self.cur.execute("SELECT count(*) FROM in_capa")

        

        if self.cur.fetchone()[0] < 1:
            self.lscapatheo = list(adminblocks.capatheodict.values())
            
            for ncol in range(len(adminblocks.mainlistblock)):
                self.dictspeed["capa_artbck{}".format(ncol)] = int(self.lscapatheo[ncol])
                self.dictspeed["capa_eanbck{}".format(ncol)] = float(self.dictspeed["capa_artbck{}".format(ncol)] / self.df_ratio["ratioaebck{}".format(ncol)])
                self.dictspeed["capa_art_avg"] = self.dictspeed.get("capa_art_avg", 0) + self.dictspeed["capa_artbck{}".format(ncol)]
                self.dictspeed["capa_ean_avg"] = self.dictspeed.get("capa_ean_avg", 0) + self.dictspeed["capa_eanbck{}".format(ncol)]
            
            self.dictspeed["capa_art_avg"] = self.dictspeed["capa_art_avg"] / len(adminblocks.mainlistblock)
            self.dictspeed["capa_ean_avg"] = self.dictspeed["capa_ean_avg"] / len(adminblocks.mainlistblock)

            useofdb.insert_dicsql(self.dictspeed, "in_capa")

        else:
            # get nb picker
            print("real capa list", list(abs(self.df_delta.iloc[-1][col] / self.df_delta['delta_time']) for col in range(1, len(self.df_delta.columns))))
            
            self.capa_real = dict(zip(self.df_capa, list(abs(self.df_delta.iloc[-1][col] / self.df_delta['delta_time']) for col in range(1, len(self.df_delta.columns)))))
            
            for k, v in self.capa_real.items():
                self.capa_real[k] = float(v * 3600/ self.df_delta['delta_time'])

            print(self.capa_real)
            useofdb.insert_dicsql(self.capa_real, "in_capa")

    def weight(self):
        #= UsingDB("./database/goatdata.db") # To Simplify if necessary
        self.ratiocol = ", ".join(["ratioaebck{}".format(x) for x in range(len(adminblocks.mainlistblock))])
        self.phrase = "SELECT %s FROM in_weight ORDER BY time_glob DESC LIMIT 1" % (self.ratiocol)
        self.df_ratio = pd.read_sql_query(self.phrase, self.conn)
        return self.df_ratio


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

        