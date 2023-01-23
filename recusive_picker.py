

def consume_time(timestock, task_list, block_list, pickername):

    if timestock == 0:
        pass
    else:

        if task_list[0] > timestock:
            
            recording[block_list[0]].append((pickername[0], timestock))
            new_sub_task = task_list[0] - timestock
            
            task_list[0] = new_sub_task
            timestock -= timestock

        
        else: #tasks_list[0] < timestock
            recording[block_list[0]].append((pickername[0], task_list[0]))
            residual_ts = timestock - task_list[0]
            timestock = residual_ts
            task_list.pop(task_list.index(task_list[0]))
            block_list.pop(block_list.index(block_list[0]))
            consume_time(residual_ts, task_list, block_list, pickername)


def picker(picker_stock):
    
    if len(picker_stock) == 0:
        pass
    
    else:
        consume_time(1, task_list, block_list, picker_stock)
        picker_stock.pop(picker_stock.index(picker_stock[0]))
        picker(picker_stock, )


picker_stock = ['Picker8', 'Picker9', 'Picker10']
tasks = {'F': 0.13, 'A': 0.8, 'C': 0.56, 'B': 0.12, 'D': 0.9, 'E': 0.49}
tasks_list = [v for v in tasks.values()]
blocks_list = [k for k in tasks.keys()]
distribution = {k:[] for k in tasks.keys()}


recording = {k:[] for k in tasks.keys()}

picker(picker_stock)
# for v in tasks.values():
#     consume_time(timestock=1, tasks_list[0]=v)
print("recording:", recording)
