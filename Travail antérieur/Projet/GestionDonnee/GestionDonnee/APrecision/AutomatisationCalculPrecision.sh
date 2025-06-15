#!/bin/bash

# ./AutomatisationCalculPrecision.sh Alan-Menet

# Nom du participant
#Participant=$1

for Element in ../Perception/*; do

    # Pour recuperer le nom du dossier
    Participant=$(basename "$Element")

    #echo $Element
    echo $Participant

    CheminPerception="../Perception/$Participant"
    CheminReproduction="../Reproduction/$Participant"




    # Vérifier si le fichier existe, le supprimer pour eviter de dupliquer les lignes
    if [ -f "$CheminPerception/CalculPulseReelle.txt" ]; then
        rm "$CheminPerception/CalculPulseReelle.txt"
    fi

    # Vérifier si le fichier existe, le supprimer pour eviter de dupliquer les lignes
    if [ -f "$CheminReproduction/CalculPulseReelle.txt" ]; then
        rm "$CheminReproduction/CalculPulseReelle.txt"
    fi


    if [ -f "$CheminPerception/ValeurPrecision.txt" ]; then
        rm "$CheminPerception/ValeurPrecision.txt"
    fi

    if [ -f "$CheminReproduction/ValeurPrecision.txt" ]; then
        rm "$CheminReproduction/ValeurPrecision.txt"
    fi

    #Calcul real time Note
    #Perception
    python3 CalculPulseSequence.py $CheminPerception/DetectionSon.txt $CheminPerception/InformationExperience.csv $CheminPerception/CalculPulseReelle.txt
    #Reproduction
    python3 CalculPlacementNoteSequence.py $CheminReproduction/DetectionSon.txt $CheminReproduction/InformationExperience.csv $CheminReproduction/CalculPulseReelle.txt ../../Sequence/RythmeBinaireFinal.txt

    #Calcul Precision
    #Perception
    python3 CalculDiffPulseSequence.py $CheminPerception/CalculPulseReelle.txt $CheminPerception/RetranscriptionInput.txt $CheminPerception/InformationExperience.csv $CheminPerception/ValeurPrecision.txt
    #Reproduction
    python3 CalculDiffPlacementNoteSequence.py $CheminReproduction/CalculPulseReelle.txt $CheminReproduction/RetranscriptionInput.txt $CheminReproduction/InformationExperience.csv $CheminReproduction/ValeurPrecision.txt

done

python3 DispersionPrecisionMeilleur.py



echo CalculPreci