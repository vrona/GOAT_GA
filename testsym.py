dict1 = {'Implant_0':1, 'Implant_1': 2, 'Chasse_0': 3}
dict2 = {'Implant_0':1.5, 'Implant_1': 2.73, 'Chasse_0': 3.04, 'Implant_0': 3.04}
set1 = set(dict1.keys())
set2 = set(dict2.keys())

if set1 ^ set2:
    print(set1 ^ set2)
else:
    print('nothing')