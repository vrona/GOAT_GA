from itertools import combinations
import numpy as np
import random
from collections import deque

class TasksPicker:
    
    def __init__(self):
        pass



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
        
        #print("Static Picker:",blocklist,'\n',"Tasks:",bufferlist,'\n',"Flying Pickers:",picker_stock)
        
        #CombPicker.combine_it([valo for valo in bufferlist.values()], 1, len(bufferlist)//2)
        #A = [valo for valo in bufferlist.values()]

        #D.emptythecup(bufferlist, picker_stock, priorityorder)
        #print(D.combine_it(A, 1, 3))

        D.taskflow(picker_stock, bufferlist, 1)
    

    """
    @param: npicker # of pickers
    @param: ntask # of tasks
    @param: t max unity of time for a single picker
    """


    def taskflow(npicker, ntask, t):
    
        max_time_bank = len(npicker) * t
        time = 0
        picker_time = 1
        q = [key for key in npicker.keys()]
        npicker = {keys: 0 for keys in npicker.keys()}

        distribution = {keys: [] for keys in npicker.keys()} # Picker8 : 0

        while time < max_time_bank:
            
            

            for k in ntask.keys():
                for name in q:

                    #while npicker[name] <= 1:
                    print(npicker[name])

                    if npicker[name] + ntask[k] < 1:

                        npicker[name] += ntask[k]
                        distribution[name].append((k, ntask[k]))
                        time += ntask[k]

                    elif npicker[name] + ntask[k] > 1:

                        inter_n = 1  - npicker[name]
                        
                        distribution[name].append((k, inter_n))
                        npicker[name] = 1
                        ntask[k] = ntask[k] - inter_n
                        time += inter_n
                        
                        time += inter_n
                        break

                print(distribution)

        #print(distribution)
        

# def pickerstock(timestock, task, picker):
#         distribution = {keys: [] for keys in picker.keys()}

#         for k, v in task.items():
#             if timestock > task[k]: # 1 - 0.13 = 0.87 - 0.8 = 0.7
#                 new_timestock = timestock - task[k]

#             elif timestock < task[k]:
#                 pass
#         return new_timestock, residual_task
            

    

if __name__ == "__main__":
    D = TasksPicker
    # data = [0.66, 0.93, 0.42]
    # D.combine_it(data, 1)
    D.doco()

    
    
# def pickerstock(picker, task, distribution):
    

# #pickerstock(picker.pop(), task[])
#     if len(picker) == 0:
#         pass
    
#     else:
#         for k, v in task.items():
#             distribution[k].append((picker[0], v))

# def task_consumption(task):
#         if len(task) == 0:
#             pass
#         else:
#             consume_time(1, task[0])
#             task.pop(task.index(task[0]))
#             print(task)

# """THIS WORKS"""
# recording = []
# def consume_time(timestock, tasks_list):

#     if timestock == 0:
#         pass
#     else:

#         if tasks_list[0] > timestock:
#             new_sub_task = tasks_list[0] - timestock # 0.49 = O.56 - 0.07
#             recording.append(timestock)
#             tasks_list.insert(0, new_sub_task)
#             timestock -= timestock
#             return tasks_list
        
#         else: #tasks_list[0] < timestock
#             recording.append(tasks_list[0])
#             print("recording #1:", recording)
#             residual_ts = timestock - tasks_list[0] # 1 - 0.13 = 0.87
#             timestock = residual_ts
#             tasks_list.pop(tasks_list.index(tasks_list[0]))
#             consume_time(residual_ts, tasks_list)

#     print("recording:", recording)
"""THIS IS AWESOME WORKS"""