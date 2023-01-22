    
    
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


recording = []
def consume_time(timestock, tasks_list):

    if timestock == 0:
        pass
    else:

        if tasks_list[0] > timestock:
            new_sub_task = tasks_list[0] - timestock # 0.49 = O.56 - 0.07
            

            recording.append(timestock)

            tasks_list.insert(0, new_sub_task)
            timestock -= timestock
            return tasks_list
        
        else: #tasks_list[0] < timestock
            recording.append(tasks_list[0])
            print("recording #1:", recording)
            residual_ts = timestock - tasks_list[0] # 1 - 0.13 = 0.87
            timestock = residual_ts
            tasks_list.pop(tasks_list.index(tasks_list[0]))
            consume_time(residual_ts, tasks_list)

    print("recording:", recording)
# def remove_task(list_task, tastocut):
#     list_task.pop

picker_stock = ['Picker8', 'Picker9', 'Picker10']
tasks = {'F': 0.13, 'A': 0.8, 'C': 0.56, 'B': 0.12, 'D': 0.9, 'E': 0.49}
tasks_list = [v for v in tasks.values()]
distribution = {k:[] for k in tasks.keys()}

# for v in tasks.values():
#     consume_time(timestock=1, tasks_list[0]=v)
tasks_list = [0.13, 0.8, 0.56, 0.12, 0.9, 0.49]
consume_time(1, tasks_list)