import pandas as pd
import os
import numpy as np


#dossier_path = '../Perception/'
dossier_path = '../Reproduction/'


def EstMusicien(identifiant): 
    # Chargez le fichier CSV dans un DataFrame
    df = pd.read_csv("../AcquisitionInformation/ModelisationInformation/participants.csv")

    # Identifiant à rechercher    # faire par rapport a l'argument
    #identifiant_recherche = 'ec47489c49b203f7ae1b6f251c5f9d3a595b2162c5062ac8261c72aefd2f5bad'
    identifiant_recherche = identifiant


    # Trouver la ligne correspondant à l'identifiant recherché
    ligne = df[df['Identifiant'] == identifiant_recherche]

    # Vérifiez si la ligne existe
    if not ligne.empty:
        # Vérifiez les colonnes "Connaissance Solfege Ecole" et "Connaissance Solfege Loisir"
        connaissance_ecole = ligne['Connaissance Solfege Ecole'].values[0]
        connaissance_loisir = ligne['Connaissance Solfege Loisir'].values[0]

        # Vérifiez si l'une des colonnes a une valeur égale à 1
        if connaissance_ecole == 1 or connaissance_loisir == 1:
            #print("Connaissance en musique")
            return 1
        else:
            #print("Aucune connaissance")
            return 2
        

# Chemin vers le dossier contenant les fichiers CSV


SequenceMusicien = np.zeros((27, 3))
CompteurMusicien = np.zeros((27, 3))

SequenceNon = np.zeros((27, 3))
CompteurNon = np.zeros((27, 3))

# Parcourir tous les fichiers dans le dossier
for fichier in os.listdir(dossier_path):
    ListeNumeroSequence = []
    TempoAssocie = []
    ComplexiteAssocie = []
    ListePulseManque = []
    ListeDelaiCommence = []
    ListeDecallageMoyen = []



    print(fichier)
    TempoMusicien = EstMusicien(fichier)
    print(TempoMusicien)
    
    with open(dossier_path + fichier + "/" + "ValeurPrecision.txt", 'r') as file:
        next(file) 
        for ligne in file:
            # Séparation de la ligne en fonction de la virgule
            colonne = ligne.split(',')

            NumeroSequence=int(colonne[0].strip())
            ListeNumeroSequence.append(NumeroSequence)

            Tempo=int(colonne[1].strip())
            TempoAssocie.append(Tempo)

            PulseManque=float(colonne[2].strip())
            ListePulseManque.append(PulseManque)
        
            DelaiCommence=float(colonne[3].strip())
            ListeDelaiCommence.append(DelaiCommence)

            DecallageMoyen=float(colonne[4].strip())
            ListeDecallageMoyen.append(DecallageMoyen)

            NoteComplexite=int(colonne[5].strip())
            ComplexiteAssocie.append(NoteComplexite)

    
    for i in range(len(ListeNumeroSequence)):
    #i correspond au compteur qui va incr
        if dossier_path == '../Perception/':
            if TempoAssocie[i] == 70:
                Tempo = 0
            elif TempoAssocie[i] == 90:
                Tempo = 1
            elif TempoAssocie[i] == 110:
                Tempo = 2
        elif dossier_path == '../Reproduction/':
            Tempo = 0

    #Construction de la matrice
    #Sequence[1] = [0,0,0]
    #Sequence[ListeNumeroSequence[i]] = [0,0,0]


        #print(SequenceMusicien[ListeNumeroSequence[i]][Tempo])
        #print(ListeNumeroSequence[i])
        #print(ListeDelaiCommence[i])


        if TempoMusicien == 1:
            SequenceMusicien[ListeNumeroSequence[i]][Tempo] = SequenceMusicien[ListeNumeroSequence[i]][Tempo] + ListeDelaiCommence[i]
            CompteurMusicien[ListeNumeroSequence[i]][Tempo] = CompteurMusicien[ListeNumeroSequence[i]][Tempo] + 1
        elif TempoMusicien == 2:
            SequenceNon[ListeNumeroSequence[i]][Tempo] = SequenceNon[ListeNumeroSequence[i]][Tempo] + ListeDelaiCommence[i]
            CompteurNon[ListeNumeroSequence[i]][Tempo] = CompteurNon[ListeNumeroSequence[i]][Tempo] + 1


#print(SequenceMusicien)
#print(CompteurMusicien)
MoyenneMusicien = np.divide(SequenceMusicien, CompteurMusicien, out=np.zeros_like(SequenceMusicien), where=CompteurMusicien!=0)
MoyenneNon = np.divide(SequenceNon, CompteurNon, out=np.zeros_like(SequenceNon), where=CompteurNon!=0)


    #Faire deux listes

"""

"""
if dossier_path == '../Perception/':
    with open("Perception/DelaiCommencementMoyenMusicien.csv", 'a') as f:
        for element in MoyenneMusicien:
            f.write("{},{},{}\n".format(element[0], element[1], element[2]))
    with open("Perception/DelaiCommencementMoyenNonMusicien.csv", 'a') as f:
        for element in MoyenneNon:
            f.write("{},{},{}\n".format(element[0], element[1], element[2]))


elif dossier_path == '../Reproduction/' : 
    with open("Reproduction/DelaiCommencementMoyenMusicien.csv", 'a') as f:
            for element in MoyenneMusicien:
                f.write("{}\n".format(element[0]))
    with open("Reproduction/DelaiCommencementMoyenNonMusicien.csv", 'a') as f:
            for element in MoyenneNon:
                f.write("{}\n".format(element[0]))
