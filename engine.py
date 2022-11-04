import pandas as pd
import sqlite3
from globaldb import ProdDB
#import pandas as pd

class Engine():


    
    def __init__(self, db):
        # self.capareal_h = 238.5
        self.conn = sqlite3.connect(db)
        self.cur = self.conn.cursor()

    #def sumit(self, dictofnum):
    #def subit(self, goal, real):

    #def trendit(self, ):

    #def delta_time(self, starting_time, ending_time):

    # def weights(self, dictofnum):

    def querygb_inputs(self):
        #self.conn = 

        self.df = pd.read_sql_query("select * from globalpick_in", self.conn)
        print(self.df.head())
        self.conn.close()

        
    
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

    db = Engine("./database/goatdata.db")
    db.querygb_inputs()
        