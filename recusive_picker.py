
# picker_stock = ['Picker8', 'Picker9', 'Picker10']
# tasks = {'F': 0.13, 'A': 0.8, 'C': 0.56, 'B': 0.12, 'D': 0.9, 'E': 0.49}
# tasks_list = [v for v in tasks.values()]
# blocks_list = [k for k in tasks.keys()]
# distribution = {k:[] for k in tasks.keys()}

class TaskBlockPicker():
    def __init__(self):
        
        self.recording = {k:[] for k in tasks.keys()}

    def consume_time(self, timestock, tasks_list, blocks_list, pickername):

        if timestock == 0:
            pass
        else:

            if tasks_list[0] > timestock:
                
                self.recording[blocks_list[0]].append((pickername[0], timestock))
                new_sub_task = tasks_list[0] - timestock
                
                tasks_list[0] = new_sub_task
                timestock -= timestock

            
            else: #tasks_list[0] < timestock
                self.recording[blocks_list[0]].append((pickername[0], tasks_list[0]))
                residual_ts = timestock - tasks_list[0]
                timestock = residual_ts
                tasks_list.pop(tasks_list.index(tasks_list[0]))
                blocks_list.pop(blocks_list.index(blocks_list[0]))
                self.consume_time(residual_ts, tasks_list, blocks_list, pickername)


    def picker(self, picker_stock):
        
        if len(picker_stock) == 0:
            pass
        
        else:
            self.consume_time(1, tasks_list, blocks_list, picker_stock)
            picker_stock.pop(picker_stock.index(picker_stock[0]))
            self.picker(picker_stock)


picker(picker_stock)
# for v in tasks.values():
#     consume_time(timestock=1, tasks_list[0]=v)
print("self.recording:", self.recording)
