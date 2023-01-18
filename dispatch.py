import pandas as pd
import numpy as np
import sqlite3
import adminblocks


class Dispatch():

    def __init__(self, db):

        try:
            self.conn = sqlite3.connect(db)
            self.cur = self.conn.cursor()
        except Exception as e:
            print(f'An error occurred: {e}.')
            exit()
    
        self.block_list = {}
        self.block_list_buffer = {}

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


    def split_pickr(self, list_block, nb_pickr_block, listofname):
        
        while bool(listofname):
            
            if nb_pickr_block >= 1:
                list_block.append((listofname[0], 1))
                listofname.pop(listofname.index(listofname[0]))
                print("show",listofname)
                nb_pickr_block -= 1
            
            if nb_pickr_block < 1:
                list_block.append(((listofname[-1]), round(float(nb_pickr_block), 2)))
                nb_pickr_block -= nb_pickr_block
                break
    
 
    def pick_in_out_block(self):

        a= self.pkrandpoly()
        
        self.df_declaredtp = pd.read_sql_query("SELECT total_pickers FROM in_globalpick ORDER BY id DESC LIMIT 1", self.conn)
        self.declaredtp = self.df_declaredtp.iloc[-1][0]
        
        listofname = list("Picker_%s"%(x) for x in range(self.declaredtp))
        
        while bool(a[0]):
            max_needed_pickr_value = max(a[0].values())
            max_needed_pickr_key = max(a[0], key=a[0].get)

            self.block_list[max_needed_pickr_key] = []

            #self.split_pickr(self.block_list[max_needed_pickr_key], max_needed_pickr_value, listofname)
            while listofname:

                if max_needed_pickr_value >= 1:
                    self.block_list[max_needed_pickr_key].append((listofname[0], 1))
                    listofname.pop(listofname.index(listofname[0]))
                    max_needed_pickr_value -= 1
                
                if max_needed_pickr_value < 1:
                    self.block_list_buffer[max_needed_pickr_key] = max_needed_pickr_value
                    max_needed_pickr_value -= max_needed_pickr_value
                

                    #print(round(float(sum(self.block_list_buffer.values())), 2))
                    
                    # if threshold < 0.51:
                    #     if not listofbuffer:
                            
                    #         listofbuffer.append(listofname[0])
                    #         self.block_list[max_needed_pickr_key].append(((listofname[0]), round(float(max_needed_pickr_value), 2)))
                    #         listofname.pop(listofname.index(listofname[0]))
                    #         max_needed_pickr_value -= max_needed_pickr_value
                                           
                    #     else:
                    #         self.block_list[max_needed_pickr_key].append(((listofbuffer[0]), round(float(max_needed_pickr_value), 2)))
                    #         max_needed_pickr_value -= max_needed_pickr_value

                    # elif threshold > 0.51:
                    #     listofbuffer.append(listofname[0])
                    #     self.block_list[max_needed_pickr_key].append(((listofbuffer[-1]), round(float(max_needed_pickr_value), 2)))
                    #     max_needed_pickr_value -= max_needed_pickr_value
                    break
  
            a[0].pop(max_needed_pickr_key)
        
        for kval, vval in self.block_list_buffer.items():
            self.block_list[kval].append((listofname[0], vval))

        print(self.block_list, '\n',self.block_list_buffer, '\n',listofname)

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

        