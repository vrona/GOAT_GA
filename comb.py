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
    # def combine_it(s, target, size):
    #     dic = {}

    #     for tup in combinations(s, size):
    #         try:
    #             dic[np.absolute(np.sum(tup) - target)].append(str(tup))
    #         except KeyError:
    #             dic[np.absolute(np.sum(tup) - target)] = [tup]

    #     buffy = [x for x in (dic[min(dic.keys())])]
    #     for y in buffy[0]:
    #         s.pop(s.index(y))
    #     buffy.append(tuple(s))
    #     return buffy


    def doco():
        a = {"A": 2.80, "B": 1.12, "C": 1.56, "D": 0.9, "E": 0.49, "F": 3.13}
        blocklist = {}
        bufferlist = {}
        picker_stock = {"Picker%s"% (x):1 for x in range(1, int(sum(a.values())+1))}
        priorityorder = []
        while a:

            max_value = max(a.values())
            max_key = max(a, key=a.get)

            blocklist[max_key] = []
            
            #bufferlist[max_key] = []
            
            
            while picker_stock:

                max_picker = [pickr for pickr, value in picker_stock.items() if value == max(picker_stock.values())]
                
                if max_value >= 1:
                    max_picker[0]
                    blocklist[max_key].append((max_picker[0],1))
                    max_value -= 1
                    picker_stock.pop(max_picker[0])

                elif max_value < 1 :
                    max_picker[0]
                    bufferlist[max_key] =  round(float(max_value), 2)
                    priorityorder.append(max_key)
                    max_value -= max_value
                    break

            a.pop(max_key)

            new_blocklist = {k:v for k,v in blocklist.items() if len(v) > 0}
            blocklist.clear()
            blocklist.update(new_blocklist)
        
        #print("Static Picker:", blocklist,'\n',"Flying Picker:", bufferlist)
        
        #CombPicker.combine_it([valo for valo in bufferlist.values()], 1, len(bufferlist)//2)
        A = [valo for valo in bufferlist.values()]

        D.emptythecup(bufferlist, picker_stock, priorityorder)
        #print(D.combine_it(A, 1, 3))

    def emptythecup(dictofflying, pickerfree, priority):
        totaltimepicker = sum(dictofflying.values())

        new_flyingpick = {}
        #= random.sample(pickerfree.keys(), 1)

       

        #while pickerfree:
        list_of_picker = [p for p in pickerfree.keys()]
        
        while list_of_picker:
            
            for x in priority:
                new_flyingpick[x] = []

                if pickerfree[pf] - dictofflying[x] > 0:
                    new_flyingpick[x].append((list_of_picker[list_of_picker.index(pf)], dictofflying[x]))
                    pickerfree[pf] = pickerfree[pf] - dictofflying[x]

                if pickerfree[pf] - dictofflying[x] < 0:
                    new_flyingpick[x].append((list_of_picker[list_of_picker.index(pf)], pickerfree[pf]))
                    dictofflying[x] = dictofflying[x] - pickerfree[pf]

                    pickerfree[pf] = 0
                    print(new_flyingpick)
                    list_of_picker.pop(list_of_picker.index(pf))
                    break
                #else:
                    #break
                    
                
                # if dictofflying[x] == 0:
                #     dictofflying.pop(x)

                        #print("1er:",dictofflying[x])
                    

                #dictofflying.pop(x)
                
                # if pickerfree[pf] == 0:
                #     pickerfree.pop(pf)
                #)

        print("New Flying Pick:", new_flyingpick)
    

if __name__ == "__main__":
    D = CombPicker
    # data = [0.66, 0.93, 0.42]
    # D.combine_it(data, 1)
    D.doco()

