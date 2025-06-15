import sys
import os
import numpy as np

if len(sys.argv) == 4:

    #IdentifiantParticipant = sys.argv[1]
    FichierEntree = sys.argv[1]
    NomFichierSortie = sys.argv[2]
    Perception = int(sys.argv[3])


    ListeNumeroSequence = []
    TempoAssocie = []
    ComplexiteAssocie = []


    Sequence = np.zeros((27, 3))
    Compteur = np.zeros((27, 3))
    


    # Ouvrir le fichier en mode lecture
    with open(FichierEntree, 'r') as file:
        next(file) 
        for ligne in file:
            # Séparation de la ligne en fonction de la virgule
            colonne = ligne.split(',')

            NumeroSequence=int(colonne[1].strip())
            ListeNumeroSequence.append(NumeroSequence)

            Tempo=int(colonne[2].strip())
            TempoAssocie.append(Tempo)

            NoteComplexite=int(colonne[3].strip())
            ComplexiteAssocie.append(NoteComplexite)


    #print(ListeNumeroSequence)


    for i in range(len(ListeNumeroSequence)):
        #i correspond au compteur qui va incr

        if TempoAssocie[i] == 70:
            Tempo = 0
        elif TempoAssocie[i] == 90:
            Tempo = 1
        elif TempoAssocie[i] == 110:
            Tempo = 2

        #Construction de la matrice
        #Sequence[1] = [0,0,0]
        #Sequence[ListeNumeroSequence[i]] = [0,0,0]

        # Valeur total
        Sequence[ListeNumeroSequence[i]][Tempo] = Sequence[ListeNumeroSequence[i]][Tempo] + ComplexiteAssocie[i]

        # Nombre de valeur
        Compteur[ListeNumeroSequence[i]][Tempo] = Compteur[ListeNumeroSequence[i]][Tempo] + 1

    """
    Je veux un truc comme ca
                        70      90      110
    Sequence 1          Moy11   Moy12  Moy13
    Sequence 2          Moy21   Moy22  Moy23
    Sequence 3 

    """
    #print(Sequence)
    #print(Compteur)

    Moyenne = np.divide(Sequence, Compteur, out=np.zeros_like(Sequence), where=Compteur!=0)

    #print(Moyenne)

    if Perception == 1:
        with open(NomFichierSortie, 'a') as f:
            for element in Moyenne:
                f.write("{:.3},{:.3},{:.3}\n".format(element[0], element[1], element[2]))
    elif Perception == 2:
        with open(NomFichierSortie, 'a') as f:
            for element in Moyenne:
                f.write("{:.3}\n".format(element[1]))


else: 
    print("Pas le bon nombre d'arguments")

