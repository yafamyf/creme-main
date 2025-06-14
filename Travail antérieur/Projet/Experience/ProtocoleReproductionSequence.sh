#!/bin/bash


Identifiant=$1
Enceinte=$2

echo $Identifiant

PathDonnee="../GestionDonnee/Reproduction/$Identifiant"

if [ -d "$PathDonnee" ]; then
    echo "Le dossier existe déjà == Conflit dans le nom"
    exit 1
else
    echo "Creation du dossier."
    mkdir -p "$PathDonnee"
    touch "$PathDonnee/InformationExperience.csv"
    touch "$PathDonnee/DetectionSon.txt"
    touch "$PathDonnee/RetranscriptionInput.txt"
    touch "$PathDonnee/MotivationFatigue.csv"
fi


pathDossier="../Sequence/SequenceRythme"
echo $pathDossier


OrdreDesSequences=$(python TirageSequence.py $pathDossier | tr -d '[],')
echo $OrdreDesSequences


tempo=90

echo "Time Absolue, Heure actuelle, NumeroSequence, Tempo, Complexite" >> "$PathDonnee/InformationExperience.csv"

echo $OrdreDesSequences

compteur=0
Incrementation=1


# Avant de commencer, on demande comment la personne se sent

while true; do
    read -p "Êtes-vous motivé à commencer l'expérience ? (Oui/Non) : " motivation
    if [[ "$motivation" == "Oui" || "$motivation" == "Non" ]]; then
        break
    else
        echo "Merci de répondre par Oui ou Non."
    fi
done

while true; do
    read -p "Ressentez-vous de la fatigue ? (Oui/Non) : " fatigue
    if [[ "$fatigue" == "Oui" || "$fatigue" == "Non" ]]; then
        echo " $compteur, $motivation, $fatigue" >> "$PathDonnee/MotivationFatigue.csv"
        break
    else
        echo "Merci de répondre par Oui ou Non."
    fi
done


# Debut des sequences

for NumeroSequence in $OrdreDesSequences
do

    echo $Incrementation

    pathSequence=("$pathDossier/SequenceNumero$NumeroSequence.mid")
    echo $pathSequence
#    TempsSleep=$((44 * 60 / $tempo))
    TempsSleep=$((20 * 60 / $tempo))

    echo $TempsSleep 

    DateRelative=$(date +%H:%M:%S.%N)
    DateAbsolue=$(date +%s.%N)

    python lancer_en_parallele.py "$pathDossier/SequenceNumero$NumeroSequence.mid" $TempsSleep $Identifiant $Enceinte $PathDonnee

    sleep 1

    while true; do
        read -n 1 -s -r -p "Veuillez donner une note sur la complexité (1-5): " touche_pressee
        if [[ $touche_pressee =~ ^[1-5]$ ]]; then
            echo "La variable est comprise entre 1 et 5."
            break
        fi
    done

    echo "$DateAbsolue, $DateRelative, $NumeroSequence, $tempo, $touche_pressee" >> "$PathDonnee/InformationExperience.csv"
    echo "Lancement de la sequence suivante"

    Incrementation=$(($Incrementation + 1))
    compteur=$((compteur + 1))


    if [[ $compteur -eq 10 || $compteur -eq 15 || $compteur -eq 20 ]]; then
        echo ""
        while true; do
            read -p "Êtes-vous motivés à continuer l'expérience et à effectuer encore quelques tâches ? (Oui/Non) : " motivation
            if [[ "$motivation" == "Oui" || "$motivation" == "Non" ]]; then
                break
            else
                echo "Merci de répondre par Oui ou Non."
            fi
        done

        while true; do
            read -p "Ressentez-vous de la fatigue ? (Oui/Non) : " fatigue
            if [[ "$fatigue" == "Oui" || "$fatigue" == "Non" ]]; then
                echo " $compteur, $motivation, $fatigue" >> "$PathDonnee/MotivationFatigue.csv"
                break
            else
                echo "Merci de répondre par Oui ou Non."
            fi
        done
        echo ""
    fi

done