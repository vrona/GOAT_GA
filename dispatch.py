import pandas as pd
import numpy as np
import sqlite3
import adminblocks

# sorted_vtasklist = []
# sorted_kblocklist = []
picker_dispatch = {}

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
        if self.real_speed == 0:
            self.pickr_needs = 0
        else:
            self.pickr_needs = round(float(self.opt_speed/self.real_speed), 2)
        return self.pickr_needs

    # computation of number of picker needed for each block and based on EAN ONLY
    def get_picker_bck_need(self):

        self.dictpkrneed_ean = {}
        self.df_speed = pd.read_sql_query("SELECT * FROM in_speed ORDER BY id DESC LIMIT 1", self.conn).drop(columns=['id'], axis=1)

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
            self.polytogive = round(float(self.declaredtp - self.totaloptipkr), 2)
            return self.optimalpkr, self.totaloptipkr, self.polytogive

 
    def dispatchme(self):
        global sorted_vtasklist, sorted_kblocklist, picker_dispatch
       
        a= self.pkrandpoly()

        sorted_kblocklist = [kblock for kblock in a[0].keys()]
        sorted_vtasklist = [task for task in a[0].values()]
        picker_dispatch = {k:[] for k in a[0].keys()}


        self.df_declaredtp = pd.read_sql_query("SELECT total_pickers FROM in_globalpick ORDER BY id DESC LIMIT 1", self.conn)
        self.declaredtp = self.df_declaredtp.iloc[-1][0]
        
        listofname = ["Picker_%s"%(x) for x in range(self.declaredtp)]

        self.picker(1, listofname)

        return picker_dispatch




    def consume_time(self, timestock, sorted_vtasklist, sorted_kblocklist, pickername):

        if timestock == 0 or len(sorted_vtasklist) == 0:
            pass
        else:

            if sorted_vtasklist[0] > timestock:
                
                picker_dispatch[sorted_kblocklist[0]].append((pickername[0], timestock))
                new_sub_task = sorted_vtasklist[0] - timestock
                
                sorted_vtasklist[0] = new_sub_task
                timestock -= timestock
                
                return timestock

            
            else: #sorted_vtasklist[0] < timestock
                picker_dispatch[sorted_kblocklist[0]].append((pickername[0], sorted_vtasklist[0]))
                residual_ts = timestock - sorted_vtasklist[0]
                timestock = residual_ts
                sorted_vtasklist.pop(sorted_vtasklist.index(sorted_vtasklist[0]))
                sorted_kblocklist.pop(sorted_kblocklist.index(sorted_kblocklist[0]))
                self.consume_time(residual_ts, sorted_vtasklist, sorted_kblocklist, pickername)

                return residual_ts


    def picker(self, time_stock, picker_stock):

        if len(picker_stock) == 0: #or time_stock == 0
            #print(picker_stock, time_stock)
            pass
        
        else:
            time_stock = self.consume_time(1, sorted_vtasklist, sorted_kblocklist, picker_stock)
            picker_stock.pop(picker_stock.index(picker_stock[0]))
            self.picker(time_stock, picker_stock)



        
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

        