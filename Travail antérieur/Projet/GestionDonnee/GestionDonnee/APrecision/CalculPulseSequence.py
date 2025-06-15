import sys

# faut dabord calculé pulse reelle, puis on peut comparer

# python3 CalculPulseSequence.py ../Perception/Alan-Menet/DetectionSon.txt ../Perception/Alan-Menet/InformationExperience.csv ../Perception/Alan-Menet/CalculPulseReelle.txt




ValeurDebutDetectionSon = []
TempoAssocie = []


if len(sys.argv) == 4:

    FichierDetectionSon = (sys.argv[1])
    FichierTempoAssocie = (sys.argv[2])
    NomFichier = sys.argv[3]


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
            Tempo=int(colonne[3].strip())
            TempoAssocie.append(Tempo)


    #print(TempoAssocie)

    for i in range(len(ValeurDebutDetectionSon)):
        
        DureePulse = 60/TempoAssocie[i]
        TimePulse=[]

        with open(NomFichier, 'a') as f:
            for NumeroPulse in range(20+1):
                TimePulse.append(ValeurDebutDetectionSon[i]+NumeroPulse*DureePulse)
            

            print(TimePulse, file=f)
            #print(TimePulse)


else:
    print("Nombre d'argument incomplet, la commande doit etre au format")
    print("programme FichierSonsDetectes FichierGlobalExperience FichierEcritureTimerPulsation")
#exit()"""
