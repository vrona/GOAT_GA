import pandas as pd
import sqlite3
import adminblocks
from datetime import datetime
from engine import Computing
from globaldb import CreateDB_OnFly

picker_dispatch = {}

class Dispatch():

    def __init__(self, db_main="./database/input_data.db", db_second="./database/dispatch_data.db"):
        """
        class dedicated to table that compute dispatch of task per block among pickers's available time. input from input_data.db, output recorded into dispatch_data.db
        """
        try:
            self.conn_main = sqlite3.connect(db_main)
            self.cur = self.conn_main.cursor()

            self.conn_second = sqlite3.connect(db_second)
            
        except Exception as e:
            print(f'An error occurred: {e}.')
            exit()


    def picker_needs(self, opt_speed, real_speed):
        """
        a helper func which computes the number of needed pickers given the real speed vs the needed speed
        """
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
        self.df_speed = pd.read_sql_query("SELECT * FROM in_speed ORDER BY id DESC LIMIT 1", self.conn_main).drop(columns=['id'], axis=1)

        for ncol in range(len(adminblocks.mainlistblock)):

            # self.opti_speedart = round(float(self.df_speed.iloc[-1]["speed_goal_artbck{}".format(ncol)]), 2)
            # self.real_speedart = round(float(self.df_speed.iloc[-1]["speed_artbck{}".format(ncol)]), 2)
            # self.pickr_need_art = self.picker_needs(self.opti_speedart, self.real_speedart)
            
            #self.dictpkrneed_ean["pkreanbck{}".format(ncol)]= self.picker_needs(
            #   round(float(self.df_speed.iloc[-1]["speed_goal_eanbck{}".format(ncol)]), 2),
            #   round(float(self.df_speed.iloc[-1]["speed_eanbck{}".format(ncol)]), 2)
            #   )
            self.dictpkrneed_ean[adminblocks.mainlistblock[ncol]]= self.picker_needs(
                round(float(self.df_speed.iloc[-1]["speed_goal_eanbck{}".format(ncol)]), 2),
                round(float(self.df_speed.iloc[-1]["speed_eanbck{}".format(ncol)]), 2)
                )

        self.totalpkrneed = round(float(sum(self.dictpkrneed_ean.values())), 2)
        return self.dictpkrneed_ean, self.totalpkrneed #self.pickr_need_art
    
    
    def pkrandpoly(self):
        """
        Pickers and Poly returns dict of optimal_picker_needed per block, total sum optimal picker, float poly to give
        """

        self.df_declaredtp = pd.read_sql_query("SELECT total_pickers FROM in_globalpick ORDER BY id DESC LIMIT 1", self.conn_main)
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


    sqlonfly = CreateDB_OnFly()
    computing = Computing()

    def real_time_stock_time(self, ls_pickr_names):
        # compute stock of time for each picker
        timerecord = datetime.now()
        limit_hour_shift = self.computing.get_shift()[0]
        real_stock_time = (limit_hour_shift - timerecord).seconds #/ 360
        rounded_real_stock_time = round(float(real_stock_time/21600),2)

        for picker in ls_pickr_names:
            self.sqlonfly.insert_real_stk_time(rounded_real_stock_time, picker)
        
        return rounded_real_stock_time


    def dispatchme(self, start_time):
        global sorted_vtasklist, sorted_kblocklist, picker_dispatch
        
        # get the number of picker at previous record
        self.sql_query = pd.read_sql_query("SELECT * FROM pickers", self.conn_second).drop(columns=['id'], axis=1)
        self.dfpickers = pd.DataFrame(self.sql_query)
        #total_pickers = int(self.dfpickers.iloc[-2]['total_pickers'])

        #  get block_name aka task, optimal_picker_needed aka value task
        a= self.pkrandpoly()
        sorted_vtasklist = []
        sorted_kblocklist = []

        # sorting the block and task by order of pickers needs
        while len(a[0]) > 0:
            sorted_vtasklist.append(max(a[0].values()))
            sorted_kblocklist.append(max(a[0],key=a[0].get))
            picker_dispatch[max(a[0],key=a[0].get)] = []
            a[0].pop(max(a[0],key=a[0].get))


        # tasks inserted
        #for task_value, task_name in zip(sorted_vtasklist, sorted_kblocklist):
        self.sqlonfly.insert_tasks(sorted_vtasklist, sorted_kblocklist)
        
        list_of_name = self.dfpickers['name'].tolist() #["Picker_%s"%(x) for x in range(self.declaredtp)]

        # copy of list of pickers before self.picker() recursive funct
        pickerz = list_of_name.copy()

        # insertion of real_time_stock_time per picker
        rounded_real_stock_time = self.real_time_stock_time(pickerz)

        # get the pickers' stock of time
        list_of_stock_of_time = [rounded_real_stock_time] * len(pickerz)

        # production of dispatch via recursive 
        self.picker(list_of_stock_of_time[0], list_of_stock_of_time, list_of_name)

        if not self.sqlonfly.ini_task_w_picker:
            for taskname in picker_dispatch.keys(): # happen at creation of task tables
                
                # create column tables of tasks
                self.sqlonfly.create_table_tasks(taskname, pickerz, "./database/dispatch_data.db")

                # insert task_time to picker to in dedicated task table
                if picker_dispatch[taskname]:
                    self.sqlonfly.insert_disp_taskpickr(taskname, picker_dispatch[taskname])
                    
                else:
                    for name_p in pickerz:
                        picker_dispatch[taskname].append((name_p, 0))

                    self.sqlonfly.insert_disp_taskpickr(taskname, picker_dispatch[taskname])


            self.sqlonfly.ini_task_w_picker = True

        else:

            self.sql_query = pd.read_sql_query("SELECT * FROM in_globalpick", self.conn_main).drop(columns=['id'], axis=1)
            self.dfbase = pd.DataFrame(self.sql_query)

            total_pickers = int(self.dfbase.iloc[-2]['total_pickers'])

            # in case number of picker more than the record before
            if len(pickerz) > total_pickers:

                pickerz_backup = pickerz.copy()
                for n_picker in range(total_pickers):
                    pickerz.pop(pickerz.index("Picker_{}".format(n_picker)))

                # update column tables of tasks
                for taskname in picker_dispatch.keys():
                    for new_picker in pickerz:
                        self.sqlonfly.update_table_picker_tasks(taskname, new_picker)
                        
                # insert task_time to picker to in dedicated task table
                self.helper_insert_dispatch(picker_dispatch, pickerz_backup)
            
            # in case number of picker less than the record before
            else:
                self.helper_insert_dispatch(picker_dispatch, pickerz)


        print("Dispatch", picker_dispatch)


        # for key_block_name, value_block_task in picker_dispatch.items():
    
        #     for values in value_block_task:
        #         """21600 seconds for 6 hours shift * portion of time needed // could also convert all .time() but SQL does not support time but datetime"""
        #         end_time = start_time + timedelta(seconds=(int(21600 * values[1])))
        #         sqlonfly.insert_picker_to_task("{}_task".format(key_block_name), values[0], values[1], start_time, end_time)


    def consume_time(self, timestock, timestock_list, sorted_vtasklist, sorted_kblocklist, pickername):
        
        if timestock == 0 or len(sorted_vtasklist) == 0:
            timestock_list.pop(timestock_list.index(timestock_list[0]))
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
                #timestock.pop(timestock.index(timestock))
                self.consume_time(timestock, timestock_list, sorted_vtasklist, sorted_kblocklist, pickername)

                return residual_ts


    def picker(self, time_stock, picker_time_stock, picker_stock):
        if len(picker_stock) == 0: #or picker_time_stock == 0
            pass
        
        else:
            time_stock = self.consume_time(picker_time_stock[0], picker_time_stock, sorted_vtasklist, sorted_kblocklist, picker_stock)
            picker_stock.pop(picker_stock.index(picker_stock[0]))
            self.picker(time_stock, picker_time_stock, picker_stock)


    def helper_insert_dispatch(self, dictbase, listofpickerz):
        for task_name in dictbase.keys():
            if dictbase[task_name]:
                self.sqlonfly.insert_disp_taskpickr(task_name, dictbase[task_name])
            
            else:
                for name in listofpickerz:
                    dictbase[task_name].append((name, 0))
                self.sqlonfly.insert_disp_taskpickr(task_name, dictbase[task_name])

        
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

        