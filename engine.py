import numpy as np
#import pandas as pd


class Engine():
    
    def __init__(self):
        self.capareal_h = 238.5
        pass

    #def sumit(self, dictofnum):
    #def subit(self, goal, real):

    #def trendit(self, ):

    #def delta_time(self, starting_time, ending_time):

    # def weights(self, dictofnum):
    
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
        