
import datetime
dictglob1 = {}
dictglob2 = {}
dictglob3 = {}
gogo = []
def auto(list1, list2):
    for k, v in zip(list1, list2):
        dictglob1[k]= v
    #print(dictglob)

def blabla(list1, list2):
    for k, v in zip(list1, list2):
        dictglob2[k]= v

dval1 = [12000,13000,14000,15000,16000,17000]
dkey1= ['art_bck1', 'art_bck2', 'art_bck3', 'art_bck4', 'art_bck5', 'art_bck6']
dval2 = [2000,3000,4000,5000,6000,7000]
dkey2= ['ean_bck1', 'ean_bck2', 'ean_bck3', 'ean_bck4', 'ean_bck5', 'ean_bck6']


auto(dkey1, dval1)
blabla(dkey2, dval2)


dictglob3 = {'time_glob': datetime.datetime.now() ,**dictglob1,**dictglob2, 'total':10}

print(gogo.append(dictglob3[key]) for key in dictglob3.__iter__())