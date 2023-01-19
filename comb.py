from itertools import combinations
import numpy as np
import random

class CombPicker:
    
    def __init__(self):
        pass

    """def combine_it(self, setofdata, target):

        dicto = {}

        for x in combinations(setofdata, target):
            try:
                dicto[np.absolute(np.sum(x) - target)].append(str(x))
            except KeyError:
                dicto[np.absolute(np.sum(x) - target)] = [x]
        print(dicto[min(dicto.keys())])"""
    def combine_it(s, target):
        dic = {}
        for tup in combinations(s, 2):
            try:
                dic[np.absolute(np.sum(tup) - target)].append(str(tup))
            except KeyError:
                dic[np.absolute(np.sum(tup) - target)] = [tup]
        print(dic[min(dic.keys())]) #


    def doco():
        a = {"A": 2.83, "B": 1.12, "C": 1.05}
        time = 5
        
        
        while a:
            blocklist = {}
            picker_stock = {"Picker%s"% (x):1 for x in range(time)}
            max_value = max(a.values())
            max_key = max(a, key=a.get)

            blocklist[max_key] = []


            #for d in range(len(picker)):
            while picker_stock:
                max_picker = [pickr for pickr, value in picker_stock.items() if value == max(picker_stock.values())]

                
                #randpickr = print(lambda x:1 if x==0 else x + random.randint(0, len(picker_stock)-1))
                max_splited_picker = max(picker_stock.values())
                max_splited_picker_key = max(picker_stock, key=picker_stock.get)

                if max_value >= picker_stock[max_picker[0]]:

                    blocklist[max_key].append((max_picker[0], picker_stock[max_picker[0]]))
                    #picker_stock[max_picker[0]] = 1 - picker_stock[max_picker[0]]

                    max_value -= 1
                    picker_stock.pop(max_picker[0])
                    max_picker.pop(max_picker.index(max_picker[0]))
                    
                print(blocklist)
                if max_value < max_splited_picker :
                    print(max_splited_picker, max_splited_picker_key)
                    blocklist[max_key].append((max_splited_picker_key, max_value))
                    picker_stock[max_splited_picker_key] = picker_stock[max_splited_picker_key] - max_value
                    max_value -= max_value

                    if picker_stock[max_splited_picker_key] == 0 :
                        picker_stock.pop(max_splited_picker_key) 


            a.pop(max_key)
        print(blocklist,'\n', picker_stock)
            
            

        
if __name__ == "__main__":
    D = CombPicker
    # data = [0.66, 0.93, 0.42]
    # D.combine_it(data, 1)
    D.doco()
