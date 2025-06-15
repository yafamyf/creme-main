import sys


# python3 CalculPlacementNoteSequence.py 
# xReproduction/Florence/Povel/TestReproductionDetectionSonFinalReprodutionFlorence-Povel2.txt 
# xReproduction/Florence/Povel/TestReproductionFinalReprodutionFlorence-Povel2.csv 
# xReproduction/Florence/Povel/CalculPulseReellePovel.txt 
# ../../Sequence/RythmeBinaireFinal.txt


# python3 CalculPlacementNoteSequence.py ../Reproduction/Alan-Menet/DetectionSon.txt ../Reproduction/Alan-Menet/InformationExperience.csv ../Reproduction/Alan-Menet/CalculPulseReelle.txt ../../Sequence/RythmeBinaireFinal.txt


ValeurDebutDetectionSon = []
TempoAssocie = []
NumeroAssocie = []


if len(sys.argv) == 5:

    FichierDetectionSon = (sys.argv[1])
    FichierTempoAssocie = (sys.argv[2])
    NomFichier = sys.argv[3]
    CheminAccesSequence = sys.argv[4]

    NombreMesure = 10


    # Ouvrir le fichier en mode lecture
    with open(FichierDetectionSon, 'r') as file:
        for ligne in file:
            #Pour enlever les espaces et \n
            ligne = float(ligne.rstrip())
            # Conversion de chaque élément en nombre et ajout à la matrice
            #ligne_matrice = [float(element.strip()) for element in ligne]
            ValeurDebutDetectionSon.append(ligne)


    # Ouvrir le fichier en mode lecture
    with open(FichierTempoAssocie, 'r') as file:
        next(file) 
        for ligne in file:
            # Séparation de la ligne en fonction de la virgule
            colonne = ligne.split(',')
            # Extraction du troisième élément (indice 2 car l'index commence à 0)
            Numero=int(colonne[2].strip())
            Tempo=int(colonne[3].strip())
            NumeroAssocie.append(Numero)
            TempoAssocie.append(Tempo)


    #print(NumeroAssocie)
    #print(TempoAssocie)

    for i in range(len(ValeurDebutDetectionSon)):       
           
            DureePulse = 60/TempoAssocie[i]
            DureeDouble = DureePulse/4

            TimePulse=[]
            #ValeurTime = 0
            ValeurTime = ValeurDebutDetectionSon[i]

            with open(CheminAccesSequence, 'r') as f:
                lignes = f.readlines()
                LigneActuel = lignes[NumeroAssocie[i]-1].strip()
                LigneActuel_sans_espaces = LigneActuel.replace(' ', '')

                # Je recupere la bonne ligne
                #print(LigneActuel)

                for nombreRepetition in range(NombreMesure):
                    for element in LigneActuel_sans_espaces:
                        if element == "1":
                            TimePulse.append(ValeurTime)
                        ValeurTime = ValeurTime+DureeDouble

                #print(TimePulse) 

            with open(NomFichier, 'a') as f:
                

                print(TimePulse, file=f)
                #print(TimePulse)


else:
    print("Nombre d'argument incomplet, la commande doit etre au format")
    print("programme FichierSonsDetectes FichierGlobalExperience FichierEcritureTimerPulsation FichierSequenceBinaire.txt")
#exit()"""
