import sys
import numpy as np

# Essens
# python3 CalculDiffPulseSequence.py xPerception/Florence/Essens/CalculPulseReelleEssens.txt xPerception/Florence/Essens/AAAInputSourisFlorence-EssensPerception.txt xPerception/Florence/Essens/AAAPerceptionFlorence-EssensPerception.csv
# python3 CalculDiffPulseSequence.py xReproduction/Florence/Essens/CalculPulseReelleEssens.txt xReproduction/Florence/Essens/BBBReproductionInputSourisFlorence-EssensReproduction.txt




# python3 CalculDiffPulseSequence.py ../Perception/Alan-Menet/CalculPulseReelle.txt ../Perception/Alan-Menet/RetranscriptionInput.txt ../Perception/Alan-Menet/InformationExperience.csv





ValeurPulseReelle = []
ValeurPulseRealise = []
OrdreSequence = []
TempoAssocie = []
ComplexiteAssocie = []

#DecallageEtalonner = 0.13283976193132072
DecallageEtalonner = 0


if len(sys.argv) == 5:
    FichierPulseReelle = sys.argv[1]
    FichierPulseRealise = sys.argv[2]
    FichierNumeroSequence = sys.argv[3]
    FichierResultat = sys.argv[4]

    # Ouvrir le fichier en mode lecture
    with open(FichierPulseReelle, 'r') as file:
        
        # Lire toutes les lignes du fichier
        #linesPulseReelle = file.readlines()
        for ligne in file:
            
            # Enleve les crochets
            ligne = ligne.strip()[1:-1]

            # Séparation de la ligne en fonction de la virgule
            elements = ligne.split(',')

            # Conversion de chaque élément en nombre et ajout à la matrice
            ligne_matrice = [float(element.strip()) for element in elements]
            
            ValeurPulseReelle.append(ligne_matrice)


    # Ouvrir le fichier en mode lecture
    with open(FichierPulseRealise, 'r') as file:
        # Lire toutes les lignes du fichier
        #linesPulseRealise = file.readlines()

        for ligne in file:
            # Enleve les crochets
            ligne = ligne.strip()[1:-1]
            # Séparation de la ligne en fonction de la virgule
            elements = ligne.split(',')
            # Conversion de chaque élément en nombre et ajout à la matrice
            ligne_matrice = [float(element.strip())+DecallageEtalonner for element in elements]
            ValeurPulseRealise.append(ligne_matrice)  


    #print(ValeurPulseRealise[0]) 


    # Ouvrir le fichier en mode lecture
    with open(FichierNumeroSequence, 'r') as file:
        next(file)
        for ligne in file:

            ligne = ligne.strip()[1:]
            # Séparation de la ligne en fonction de la virgule
            elements = ligne.split(',')
        
            numero_sequence = int(elements[2])
            OrdreSequence.append(numero_sequence)

            TempoSequence = int(elements[3])
            TempoAssocie.append(TempoSequence)

            ComplexiteSequence = int(elements[4])
            ComplexiteAssocie.append(ComplexiteSequence)


MoyenneDifferenceJustesse = []
MoyenneDifferenceDebut = []

ValeurPlusPetit = []
ValeurPlusGrand = []

IndicePlusPetit = []
IndicePlusGrand = []

DifferenceJustessePoid = []




with open(FichierResultat, 'a') as f:

    print("NumeroDeSequence,Tempo,PulsationManquee,DelaiAvantDeCommencer, DecalageMoyen,Complexite", file=f)


    for NumeroLigne in range(len(ValeurPulseRealise)):

        TotalDifference = 0
        TotalPoid = 1
        ListeDifference = []


        PulseSequence = ValeurPulseReelle[NumeroLigne]
        PulseParticipant = ValeurPulseRealise[NumeroLigne]

        if ValeurPulseRealise[NumeroLigne][0] == 1:
            MoyenneDifferenceJustesse.append(1)
            DifferenceJustessePoid.append(1)
            continue

        
        #MoyenneDifferenceDebut.append(abs(ValeurDebutSon[NumeroLigne]-PulseSequence[0]))
        #Delay=abs(ValeurDebutSon[NumeroLigne]-PulseSequence[0])

        """
        PulseSequence[0] = la premiere pulsation attendue
            == il n'y a plus de delai
        """


        for Pulse in range(len(PulseParticipant)):
            for Referenciel in range(len(PulseSequence)-1):
                if (PulseParticipant[Pulse]) >= PulseSequence[Referenciel] and (PulseParticipant[Pulse]) <= PulseSequence[Referenciel+1]:
                    Difference = min(abs((PulseParticipant[Pulse])-PulseSequence[Referenciel]), abs((PulseParticipant[Pulse])-PulseSequence[Referenciel+1]))
                    ListeDifference.append(Difference)
                    #Creation de poid
                    TotalDifference = TotalDifference + (Difference * (Pulse))
                    TotalPoid = TotalPoid + (Pulse)
        
        if len(ListeDifference) > 0 :
            PlusPetiteDiff = min(ListeDifference) 
            IndicePetitCorrespondant = ListeDifference.index(PlusPetiteDiff)

            PlusGrandeDiff = max(ListeDifference)  
            IndiceGrandCorrespondant = ListeDifference.index(PlusGrandeDiff)


            ValeurPlusPetit.append(PlusPetiteDiff)    
            IndicePlusPetit.append(IndicePetitCorrespondant)

            ValeurPlusGrand.append(PlusGrandeDiff)
            IndicePlusGrand.append(IndiceGrandCorrespondant)

            #print(ListeDifference)
            ValeurMoyenne = (sum(ListeDifference)) / (len(ListeDifference))
            MoyenneDifferenceJustesse.append(ValeurMoyenne)

            DifferenceJustessePoid.append(TotalDifference/TotalPoid)

            Resultat="{},{},{},{},{},{}".format(OrdreSequence[NumeroLigne], TempoAssocie[NumeroLigne], len(PulseSequence)-len(PulseParticipant), PulseParticipant[0]-PulseSequence[0],ValeurMoyenne,ComplexiteAssocie[NumeroLigne])

            print(Resultat,file=f)