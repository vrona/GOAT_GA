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


"""FORMER DISPATCH"""
def bankofpicker(self): # MOTEUR DE DISPATCH BASE SUR LE RESTANT

        a= self.pkrandpoly()
        
        print("THIS A:", a)
        self.df_declaredtp = pd.read_sql_query("SELECT total_pickers FROM in_globalpick ORDER BY id DESC LIMIT 1", self.conn)
        self.declaredtp = self.df_declaredtp.iloc[-1][0]
    while bool(a[0]):
                max_needed_pickr_value = max(a[0].values())
                max_needed_pickr_key = max(a[0], key=a[0].get)

                self.block_list[max_needed_pickr_key] = []
                dictofname = {"Picker_%s"%(x):1 for x in range(self.declaredtp)}
                print(dictofname)
                #self.split_pickr(self.block_list[max_needed_pickr_key], max_needed_pickr_value, listofname)
                #while listofname:
                for x in range(self.declaredtp):

                    if max_needed_pickr_value - dictofname["Picker_%s"%(x)] >= 0:
                        self.block_list[max_needed_pickr_key].append(("Picker_%s"%(x), dictofname["Picker_%s"%(x)]))
                        dictofname.pop("Picker_%s"%(x))
                        max_needed_pickr_value -= 1

                    if max_needed_pickr_value - dictofname["Picker_%s"%(x)] < 0:
                        self.block_list[max_needed_pickr_key].append(("Picker_%s"%(x), max_needed_pickr_value))
                        dictofname["Picker_%s"%(x)] = max_needed_pickr_value - dictofname["Picker_%s"%(x)]
                        
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
                    print("block_list:", self.block_list)
                a[0].pop(max_needed_pickr_key)
            echoof = self.block_list_buffer.values()
            print("echoof:", echoof)
            # for kval, vval in self.block_list_buffer.items():
            #     self.block_list[kval].append((listofname[0], vval))

            #print(self.block_list, '\n',self.block_list_buffer, '\n',listofname)