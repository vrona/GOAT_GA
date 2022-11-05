import pandas as pd
import sqlite3

listofoutdoor = ["C Chasse", "C SportCo", "D Glisse", "D Running", "PFECA", "Implant"]
listofhopside = ["Bloc E", "Prio E", "Bloc E", "Prio V", "PFECA", "Implant"]

class Blocks:
    
    def __init__(self):
        # super().__init__()
        # self.listofblocks = []
        # self.dictarticle = {}
        # self.dictean = {}
        pass


    def blocdataframe(self):
        self.listofblocks = ["C Chasse", "C SportCo", "D Glisse", "D Running", "PFECA", "Implant"] #listofblocks
        self.listofids = list(self.listofblocks.index(x) for x in self.listofblocks)
        self.data = {'id': self.listofids, 'name': self.listofblocks}
        self.df = pd.DataFrame(self.data, columns=['id','name'])
        return self.df.to_string()



bloc = Blocks()
bloc.blocdataframe()