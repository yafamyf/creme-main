import numpy as np
import sys
import csv
import CorrelationSpearman
from scipy import stats


#CheminDonnees = "EDAMusicienParSequence.csv"
CheminDonnees = "EDANonMusicienParSequence.csv"


ComplexitePercuPerception = [
    2.363636364,
    2.727272727,
    2.545454545,
    2.181818182,
    1.636363636,
    1.727272727,
    1.727272727,
    2.454545455,
    2.363636364,
    2.545454545,
    1.909090909,
    1.454545455,
    1.727272727,
    2,
    2.636363636,
    3.181818182,
    2.181818182,
    2.363636364,
    1.818181818,
    2.272727273,
    3,
    2.727272727,
    2.727272727,
    2.454545455,
    2.818181818,
    2.545454545
]


ComplexitePercuReproduction = [
    2.18,
2.36,
3.09,
2.73,
2.91,
2.20,
2.91,
2.73,
2.55,
2.60,
2.55,
2.27,
1.91,
2.09,
2.73,
2.36,
2.45,
2.82,
3.45,
2.64,
3.36,
3.09,
2.73,
3.27,
3.09,
3.00,

]



ComplexiteEssens95 = [
    3.1,
    3.2,
    3.1,
    2.6,
    2.8,
    2.5,
    2.4,
    3.2,
    2.4,
    2.12,
    2.08,
    1.8,
    2.44,
    3,
    2.04,
    2.6,
    3.08,
    2.56,
    2.56,
    2.84,
    3.6,
    3.28,
    3.52,
    3.6,
    2.88,
    4
]




# Ouvrir le fichier en mode lecture
with open(CheminDonnees, 'r') as file:
    # Créer un lecteur CSV
    csv_reader = csv.reader(file)
    
    # Lire toutes les lignes en tant que listes de floats
    lines_list = [[float(value) for value in row] for row in csv_reader]
"""
print(len(lines_list))
print(lines_list[0])
print(len(ComplexitePercu))
"""

for element in lines_list:
    #CorrelationSpearman.CalculSpearman(element,ComplexitePercuPerception)
    CorrelationSpearman.CalculSpearman(element,ComplexitePercuReproduction)


    #CorrelationSpearman.CalculSpearman(element,ComplexiteEssens95)


