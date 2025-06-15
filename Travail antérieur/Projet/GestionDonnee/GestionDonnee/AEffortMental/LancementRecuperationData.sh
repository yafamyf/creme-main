#!/bin/bash


for Element in ../EDA/*; do
    if [ -d "$Element" ]; then
        Participant=$(basename "$Element")

        PathEDAParticipant="../EDA/$Participant/EDA.csv"
        PathPerceptionParticipant="../Perception/$Participant/InformationExperience.csv"
        PathRepreductionParticipant="../Reproduction/$Participant/InformationExperience.csv"

        python3 LectureDonneeEDA.py $PathPerceptionParticipant $PathEDAParticipant 1



        #Perception
        #python3 LectureDonneeEDA.py $Participant $PathEDAParticipant 1

        #Repreduction
        #python3 LectureDonneeEDA.py $Participant $PathEDAParticipant 2
    fi
done
