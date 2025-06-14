
import sys 
import os
import random
#Le passer en parametre avec l'appel du programme en shell



dossier = sys.argv[1]
#fichiers = os.listdir(dossier)
fichiers = [f for f in os.listdir(dossier) if f.endswith('.mid')]

NombreElement = len(fichiers)
ListeSequence = list(range(1, 1+NombreElement))

# Mélanger la liste
random.shuffle(ListeSequence)

# Afficher la liste mélangée
print(ListeSequence)

