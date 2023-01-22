    
    
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
picker_stock = ['Picker8', 'Picker9', 'Picker10']
tasks = {'F': 0.13, 'A': 0.8, 'C': 0.56, 'B': 0.12, 'D': 0.9, 'E': 0.49}
tasks_list = [v for v in tasks.values()]
blocks_list = [k for k in tasks.keys()]
distribution = {k:[] for k in tasks.keys()}

recording = {k:[] for k in tasks.keys()}

def consume_time(timestock, tasks_list, blocks_list, pickername):

    if timestock == 0:
        pass
    else:

        if tasks_list[0] > timestock:
            
            recording[blocks_list[0]].append((pickername[0], timestock))
            new_sub_task = tasks_list[0] - timestock
            
            tasks_list[0] = new_sub_task
            timestock -= timestock

        
        else: #tasks_list[0] < timestock
            recording[blocks_list[0]].append((pickername[0], tasks_list[0]))
            residual_ts = timestock - tasks_list[0]
            timestock = residual_ts
            tasks_list.pop(tasks_list.index(tasks_list[0]))
            blocks_list.pop(blocks_list.index(blocks_list[0]))
            consume_time(residual_ts, tasks_list, blocks_list, pickername)


def picker(picker_stock):
    
    if len(picker_stock) == 0:
        pass
    
    else:
        consume_time(1, tasks_list, blocks_list, picker_stock)
        picker_stock.pop(picker_stock.index(picker_stock[0]))
        picker(picker_stock)


picker(picker_stock)
# for v in tasks.values():
#     consume_time(timestock=1, tasks_list[0]=v)
print("recording:", recording)
