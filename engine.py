import pandas as pd
import numpy as np
import sqlite3
import globaldb
from globaldb import UsingDB
import adminblocks
from math import ceil
import datetime
#import time

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
        
        # doing some maths to get total, get_weight

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
        self.dfbase = self.veryglobal.drop(columns=['id', 'total_pickers'], axis=1)

        self.dfbase['time_glob'] = pd.to_datetime(self.dfbase['time_glob'])

        if len(self.dfbase) > 1:
            self.deltakey = globaldb.ls_delta

            self.df_diff = self.dfbase.diff(axis=0)
            self.df_diff.dropna(inplace=True)

            # self.dict_diff = self.df_diff.to_dict()
            self.listinter = list(self.df_diff.iloc[-1][x] for x in range(len(self.df_diff.columns))) # new list

            self.listinter[0] = self.listinter[0].seconds #timedelta convert into seconds

            for v in range(len(self.listinter)):
                self.listinter[v] = int(self.listinter[v])

            self.lastdict = dict(zip(self.deltakey, list(self.listinter[val] for val in range(1, len(self.listinter)))))  #new dict
            self.lastdict['delta_time'] = self.listinter[0]

            useofdb.insert_dicsql(self.lastdict, "delta_table")

    def get_shift(self):
        today = datetime.datetime.today()
        self.night = (datetime.time(2, 45,0), "night")
        self.morning = (datetime.datetime(today.year, today.month, today.day, 12, 45, 0), "morning")
        self.afternoon = (datetime.datetime(today.year, today.month, today.day, 19, 45, 1), "afternoon")
        self.eve = (datetime.datetime(today.year, today.month, today.day, 19, 45, 2), "evening")

        if datetime.datetime.now().time() < datetime.time(2, 5, 0):
            return self.night
        elif datetime.time(5, 5, 0) < datetime.datetime.now().time() < datetime.time(12, 45, 0):
            return self.morning
        elif datetime.time(12, 45, 1) < datetime.datetime.now().time() < datetime.time(19, 45, 0):
            return self.afternoon
        elif datetime.time(19, 45, 0) < datetime.datetime.now().time() < datetime.time(23, 59, 59):
            return self.eve

    def new_goal(self):

        self.delta_prod()
        self.shiftdata = self.get_shift()
         
        self.shiftendtime = self.shiftdata[0] # limit of shift recall [1] is the shift's name
        self.getgoaltime = self.shiftendtime - pd.to_datetime(globaldf['time_glob'].values[-1])
        self.getgoaltime = self.getgoaltime.seconds

        useofdb = UsingDB("./database/goatdata.db") # To Simplify if necessary
        self.goalkey = globaldb.ls_goal_g # list of futur keys' dict

        self.sql_weight = pd.read_sql_query("SELECT * FROM in_weight ORDER BY time_glob DESC LIMIT 1", self.conn)
        self.dfweight = pd.DataFrame(self.sql_weight) #, columns=[key for key in dictbase.keys()]

        # check the length of goalpick table
        self.cur.execute("SELECT count(*) FROM goalpick")

        if self.cur.fetchone()[0] < 1:
             # query art, ean 1st inputs

            self.dfglobal = globaldf.drop(columns=['time_glob', 'total_pickers'], axis=1)

            if adminblocks.setthegoal[0] > 0:
                self.weigthvol = adminblocks.setthegoal[0] / np.uint32(self.dfweight['total_art_topick']).item()
                
                self.dictgoal = dict(zip(self.goalkey, list(int(self.weigthvol * self.dfglobal[col].values[-1]) for col in self.dfglobal.columns)))
                self.dictgoal['time_left'] = self.getgoaltime
                useofdb.insert_dicsql(self.dictgoal, "goalpick")
                return self.dictgoal.items()

            elif adminblocks.setthegoal[1] > 0:
                self.percent = adminblocks.setthegoal[1] / 100
  
                self.dictgoal = dict(zip(self.goalkey,  list(int(self.percent * self.dfglobal[col].values[-1]) for col in self.dfglobal.columns)))
                self.dictgoal['time_left'] = self.getgoaltime
                useofdb.insert_dicsql(self.dictgoal, "goalpick")
                return self.dictgoal

            else:
                self.dictgoal = dict(zip(self.goalkey, list(self.dfglobal[col].values[-1] for col in self.dfglobal.columns)))
                for k, v in self.dictgoal.items():
                    self.dictgoal[k] = int(v)
                self.dictgoal['time_left'] = self.getgoaltime
                useofdb.insert_dicsql(self.dictgoal, "goalpick")
                return self.dictgoal

        else:
            self.newdictgoal = {}
            # get previous goal and picking datas
            self.sql_input = pd.read_sql_query("SELECT * FROM in_globalpick ORDER BY time_glob DESC LIMIT 1", self.conn)
            #self.time = self.sql_input['time_glob'].values[-1]

            self.sql_goal = pd.read_sql_query("SELECT * FROM goalpick ORDER BY time_left DESC LIMIT 1", self.conn)

            self.sql_goal = self.sql_goal.drop(columns=['id','time_left'], axis=1)
           
            self.sql_delta = pd.read_sql_query("SELECT * FROM delta_table ORDER BY id DESC LIMIT 1", self.conn)
            self.df_delta = self.sql_delta.drop(columns=['id','delta_time'], axis=1)
            
            self.addition = pd.DataFrame(columns=self.goalkey)

            for indexofit, names in enumerate(self.goalkey):
                 
                self.addition.loc[0, names] = self.sql_goal.iloc[-1][indexofit].item() + self.df_delta.iloc[-1][indexofit].item()

            self.newdictgoal = dict(zip(self.goalkey, list(self.addition[col].values[-1] for col in self.goalkey)))

            # convert figures value as int
            for k, v in self.newdictgoal.items():
                self.newdictgoal[k] = int(v)

            self.newdictgoal['time_left'] = self.getgoaltime
            
            useofdb.insert_dicsql(self.newdictgoal, "goalpick")

    def get_weight(self):
        #= UsingDB("./database/goatdata.db") # To Simplify if necessary
        self.ratiocol = ", ".join(["ratioaebck{}".format(x) for x in range(len(adminblocks.mainlistblock))])
        self.phrase = "SELECT %s FROM in_weight ORDER BY time_glob DESC LIMIT 1" % (self.ratiocol)
        self.df_ratio = pd.read_sql_query(self.phrase, self.conn)
        return self.df_ratio

    def speedtocatch(self, ncol):

        self.df_spgoal = pd.read_sql_query("SELECT * FROM goalpick ORDER BY id DESC LIMIT 1", self.conn).drop(columns=['id'], axis=1)

        self.speed_goal_art = round(float(self.df_spgoal.iloc[-1]["goal_artbck{}".format(ncol)] / self.df_spgoal['time_left'].values[-1] * 3600), 3)
        self.speed_goal_ean = round(float(self.df_spgoal.iloc[-1]["goal_eanbck{}".format(ncol)] / self.df_spgoal['time_left'].values[-1] * 3600), 3)

        return self.speed_goal_art, self.speed_goal_ean


    def speedness(self):
        self.dictspeed = {}
        self.df_ratio = self.get_weight()
        useofdb = UsingDB("./database/goatdata.db") # To Simplify if necessary

        # check the length of goalpick table
        self.cur.execute("SELECT count(*) FROM in_speed")

        if self.cur.fetchone()[0] < 1:
            self.lsspeedtheo = list(adminblocks.speedtheodict.values())
            
            for ncol in range(len(adminblocks.mainlistblock)):
                self.dictspeed["speed_artbck{}".format(ncol)] = int(self.lsspeedtheo[ncol])
                self.dictspeed["speed_eanbck{}".format(ncol)] = round(float(self.dictspeed["speed_artbck{}".format(ncol)] / self.df_ratio["ratioaebck{}".format(ncol)].values[-1]), 3)

                self.dictspeed["speed_goal_artbck{}".format(ncol)], self.dictspeed["speed_goal_eanbck{}".format(ncol)] = self.speedtocatch(ncol)

                self.dictspeed["speed_art_avg"] = self.dictspeed.get("speed_art_avg", 0) + self.dictspeed["speed_artbck{}".format(ncol)]
                self.dictspeed["speed_ean_avg"] = self.dictspeed.get("speed_ean_avg", 0) + self.dictspeed["speed_eanbck{}".format(ncol)]
            
            self.dictspeed["speed_art_avg"] = self.dictspeed["speed_art_avg"] / len(adminblocks.mainlistblock)
            self.dictspeed["speed_ean_avg"] = self.dictspeed["speed_ean_avg"] / len(adminblocks.mainlistblock)

            useofdb.insert_dicsql(self.dictspeed, "in_speed")
            return self.dictspeed

        else:
            self.df_delta = pd.read_sql_query("SELECT * FROM delta_table", self.conn).drop(columns=['id'], axis=1)
            self.df_speed = pd.read_sql_query("SELECT * FROM in_speed", self.conn).drop(columns=['id'], axis=1)

            # get nb picker
            self.speed_real = dict(zip(globaldb.ls_speed_artean, list(abs(self.df_delta.iloc[-1][col] / self.df_delta['delta_time'].values[-1]) for col in range(1, len(self.df_delta.columns)))))

            for k, v in self.speed_real.items():
                self.speed_real[k] = round(float(v * 3600), 3)

            for ncol in range(len(adminblocks.mainlistblock)):
                self.speed_real["speed_art_avg"] = self.speed_real.get("speed_art_avg",0) + self.speed_real["speed_artbck{}".format(ncol)]
                self.speed_real["speed_ean_avg"] = self.speed_real.get("speed_ean_avg",0) + self.speed_real["speed_eanbck{}".format(ncol)]
                self.speed_real["speed_goal_artbck{}".format(ncol)], self.speed_real["speed_goal_eanbck{}".format(ncol)] = self.speedtocatch(ncol)

            self.speed_real["speed_art_avg"] = self.speed_real["speed_art_avg"] / len(adminblocks.mainlistblock)
            self.speed_real["speed_ean_avg"] = self.speed_real["speed_ean_avg"] / len(adminblocks.mainlistblock)

            useofdb.insert_dicsql(self.speed_real, "in_speed")
            return self.speed_real

    def total(self):
        'totals_out'

        """
        id 
        timeofrecord == FOREIGN KEY (timeofrecord) REFERENCES in_globalpick (time_glob))
        total_prelev == sum_delta
        delta_speed == diff speed goal - speed real
        block_predic == ax + b
        total_predic == sum block_predic
        """

    def optimal_speed(self, vol_todo, time_left):
        self.vol_todo = vol_todo
        self.time_left = time_left
        self.opti_speed = round(float(self.vol_todo/self.time_left), 3)
        return self.opti_speed

    def truck_time(self):
        pass
    

class Dispatch():

    def __init__(self, db):

        try:
            self.conn = sqlite3.connect(db)
            self.cur = self.conn.cursor()
        except Exception as e:
            print(f'An error occurred: {e}.')
            exit()
    
    def picker_needs(self, opt_speed, real_speed):
        self.opt_speed = opt_speed
        self.real_speed = real_speed
        self.pickr_needs = round(float(self.opt_speed/self.real_speed), 2)
        return self.pickr_needs

    # computation of number of picker needed for each block and based on EAN ONLY
    def get_picker_bck_need(self):

        self.dictpkrneed_ean = {}
        self.df_speed = pd.read_sql_query("SELECT * FROM in_speed ORDER BY id DESC LIMIT 1", self.conn).drop(columns=['id'], axis=1)
        print(self.df_speed)
        for ncol in range(len(adminblocks.mainlistblock)):

            # self.opti_speedart = round(float(self.df_speed.iloc[-1]["speed_goal_artbck{}".format(ncol)]), 2)
            # self.real_speedart = round(float(self.df_speed.iloc[-1]["speed_artbck{}".format(ncol)]), 2)
            # self.pickr_need_art = self.picker_needs(self.opti_speedart, self.real_speedart)
            
            #self.dictpkrneed_ean["pkreanbck{}".format(ncol)]= self.picker_needs(round(float(self.df_speed.iloc[-1]["speed_goal_eanbck{}".format(ncol)]), 2), round(float(self.df_speed.iloc[-1]["speed_eanbck{}".format(ncol)]), 2))
            self.dictpkrneed_ean[adminblocks.mainlistblock[ncol]]= self.picker_needs(round(float(self.df_speed.iloc[-1]["speed_goal_eanbck{}".format(ncol)]), 2), round(float(self.df_speed.iloc[-1]["speed_eanbck{}".format(ncol)]), 2))

        self.totalpkrneed = round(float(sum(self.dictpkrneed_ean.values())), 2)
        return self.dictpkrneed_ean, self.totalpkrneed #self.pickr_need_art

    def pkrandpoly(self):
        self.weighted = {}
        self.df_declaredtp = pd.read_sql_query("SELECT total_pickers FROM in_globalpick ORDER BY id DESC LIMIT 1", self.conn)
        self.declaredtp = self.df_declaredtp.iloc[-1][0]
        self.optimalpkr, self.totaloptipkr = self.get_picker_bck_need()
        
        if self.declaredtp < self.totaloptipkr:
            for ncol in range(len(adminblocks.mainlistblock)):
                
                #self.optimalpkr["pkreanbck{}".format(ncol)] = round(float((self.optimalpkr["pkreanbck{}".format(ncol)] / self.totaloptipkr) * self.declaredtp), 2)
                self.optimalpkr[adminblocks.mainlistblock[ncol]] = round(float((self.optimalpkr[adminblocks.mainlistblock[ncol]] / self.totaloptipkr) * self.declaredtp), 2)
                self.polyneeded = round(float(self.declaredtp - self.totaloptipkr), 2)
            return self.optimalpkr, self.totaloptipkr, self.polyneeded
        else:
            self.polyneeded = round(float(self.declaredtp - self.totaloptipkr), 2)
            return self.optimalpkr, self.totaloptipkr, self.polyneeded







    """
    PICKERS DISTRIBUTION
    Total Picker * Ean weights
    Total Picker * Articles weights

    TRENDING
    - Trend pick/hour
    - Trend pick/all_passed_hours
    Forecast Picking next hour and shift  -> y = ax + b
    
    DELTA speedCITIF
    speedness goal/h - real speedness picked/h
    Forecast : total speedness - Trend pick/all_passed_hours
   
    POLY FUNCTION
    delta time = time ending shift - time of record
    """

        