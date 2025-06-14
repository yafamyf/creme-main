#!/bin/bash


Identifiant=$1
Enceinte=$2


pathDossier="../Sequence/SequenceIntroductionPerception/90"

echo $pathDossier
 

PathDonnee="../GestionDonnee/IntroductionPerception/$Identifiant"

echo "pathDonnee : $PathDonnee"

if [ -d "$PathDonnee" ]; then
    echo "Le dossier existe déjà == Conflit dans le nom"
    exit 1
else
    echo "Creation du dossier."
    mkdir -p "$PathDonnee"
    touch "$PathDonnee/RetranscriptionInput.txt"
    touch "$PathDonnee/DetectionSon.txt"

fi



for NumeroSequence in 1 2 3
do

    pathSequence=("$pathDossier/SequenceNumero$NumeroSequence.mid")
    echo "pathSequence : $pathSequence"
    TempsSleep=$((20 * 60 / 90))
    echo "Délai : $TempsSleep"

    DateRelative=$(date +%H:%M:%S.%N)
    DateAbsolue=$(date +%s.%N)

    # Lancement en parallèle de la lecture du fichier MIDI et de la collecte des percussions
    echo "Lancement de lancer_en_parallele.py"
    python lancer_en_parallele.py "$pathDossier/SequenceNumero$NumeroSequence.mid" $TempsSleep $Identifiant $Enceinte $PathDonnee

    sleep 2

    while true; do
        read -n 1 -s -r -p "Veuillez donner une note sur la complexité (1-5): " touche_pressee
        if [[ $touche_pressee =~ ^[1-5]$ ]]; then
            echo "La variable est comprise entre 1 et 5."
            break
        fi
    done

    echo "Lancement de la sequence suivante"

done