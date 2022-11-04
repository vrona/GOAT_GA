#from tkinter import *
from outdoor import PickGAApp

listofblock = ["Sport Co", "Chasse", "Glisse", "Running", "Implant"]
# Part
block = PickGAApp(listofblock)
block()

# start app


"""
DB:
13 > 14	H1	0,75
14 > 15	H2	1
15 > 16	H3	1
16 > 17	H4	0,75
17 > 18	H5	0,75
18 > 19	H6	1
19 > 19.40	H7	0,67
Total : 5,92

1 - Quelle team ? C2 ou C3
2 - Quelle heure (H0) ?
    Articles / block ?
    EAN / block ?
    return Weights Articles & EAN
    Nb total Pickers présents ? ici répartition des minutes disponibles par blocks via Walker

    3 Modes :
    - Beast
    - Champ
    - Fire
    - Pure Prod.
    - Pure Proms.

3
    - "Répart initiale Pickers" : Affiche la répartition par block en somme des floats / 355,2 minutes
    - Heures en float disponible (H0-H7).
    - Volumes Total Article et EAN Restant

4 - Heure H1
    Articles / block ?
    EAN / block ?
    return Weights Articles & EAN
    - "Répart initiale Pickers" : Affiche la répartition par block en somme des floats / 310,2 minutes
    - Heures en float disponible (H1-H7).
    - Volumes Total Article et EAN Restant

5 - TOUJOURS H1
    recommendation : Block SportCo a besoin X Picker + xx minutes. Disponibilité pour autre Block : Y X Picker + 3 heures + xx minutes.

6 - Prevision Shift
    linear regression sur Vol = slope * minutes + articles init
"""
