#!/bin/bash

# Vérifier si le fichier existe, le supprimer pour eviter de dupliquer les lignes
if [ -d "./Note" ]; then
    rm -r "./Note"
    mkdir "./Note"
fi

# Vérifier si le fichier existe, le supprimer pour eviter de dupliquer les lignes
if [ -f "./MoyenneNotePerceptionMusicien.csv" ]; then
    rm "./MoyenneNotePerceptionMusicien.csv"
    rm "./MoyenneNotePerceptionNonMusicien.csv"

fi

    # Vérifier si le fichier existe, le supprimer pour eviter de dupliquer les lignes
if [ -f "./MoyenneNoteReproductionMusicien.csv" ]; then
    rm "./MoyenneNoteReproductionMusicien.csv"
    rm "./MoyenneNoteReproductionNonMusicien.csv"

fi



for Element in ../Perception/*; do

    # Pour recuperer le nom du dossier
    Participant=$(basename "$Element")

    #echo $Element
    echo $Participant

    CheminNotePerception="../Perception/$Participant"
    CheminNoteReproduction="../Reproduction/$Participant"

    echo $Participant
    echo $CheminNotePerception/InformationExperience.csv
    echo ./NotePerception.csv


    #Calcul real time Note
    #Perception
    python3 RecuperationNoteMusicien.py $Participant $CheminNotePerception/InformationExperience.csv ./Note/NotePerception.csv
    
    #Reproduction
    python3 RecuperationNoteMusicien.py $Participant $CheminNoteReproduction/InformationExperience.csv ./Note/NoteReproduction.csv

done


python3 MoyenneComplexiteParticipant.py ./Note/NotePerception-Musicien.csv ./MoyenneNotePerceptionMusicien.csv 1
python3 MoyenneComplexiteParticipant.py ./Note/NotePerception-NonMusicien.csv ./MoyenneNotePerceptionNonMusicien.csv 1

python3 MoyenneComplexiteParticipant.py ./Note/NoteReproduction-Musicien.csv ./MoyenneNoteReproductionMusicien.csv 2
python3 MoyenneComplexiteParticipant.py ./Note/NoteReproduction-NonMusicien.csv ./MoyenneNoteReproductionNonMusicien.csv 2

echo RecupeNote

