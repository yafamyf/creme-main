#!/bin/bash
Identifiant=$1
Enceinte=$2

echo $Identifiant

PathDonnee="../GestionDonnee/Perception/$Identifiant"

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


pathDossier="../Sequence/SequencePulse"

echo $pathDossier

OrdreDesSequences=$(python TirageSequence.py "$pathDossier/90" | tr -d '[],')

echo $OrdreDesSequences 

#tempo_aleatoire=$(shuf -e 70 90 110 -n 1) -> shuf pas pratique sur mac

options=(70 90 110)
# index aléatoire entre 0 et 2
index=$((RANDOM % ${#options[@]}))
tempo_aleatoire=${options[$index]}

tempo_actuel=-1

echo $tempo_aleatoire

echo "Time Absolue, Heure actuelle, NumeroSequence, Tempo, Complexite" >> "$PathDonnee/InformationExperience.csv"

compteur=0



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




for NumeroSequence in $OrdreDesSequences
do

    while [ $tempo_aleatoire -eq $tempo_actuel ]; do
        # On force le tempo à varier à chaque séquence
        # tempo_aleatoire=$(shuf -e 70 90 110 -n 1)
        index=$((RANDOM % ${#options[@]}))
        tempo_aleatoire=${options[$index]}
    done
    tempo_actuel=$tempo_aleatoire

    pathSequence=("$pathDossier/$tempo_actuel/SequenceNumero$NumeroSequence.mid")
    echo $pathSequence
    TempsSleep=$((20 * 60 / $tempo_actuel))
    echo "Délai : $TempsSleep"

    DateRelative=$(date +%H:%M:%S.%N)
    DateAbsolue=$(date +%s.%N)

    python lancer_en_parallele.py "$pathSequence" $TempsSleep $Identifiant $Enceinte $PathDonnee

    sleep 2

    while true; do
        read -n 1 -s -r -p "Veuillez donner une note sur la complexité (1-5): " touche_pressee
        if [[ $touche_pressee =~ ^[1-5]$ ]]; then
            echo "La variable est comprise entre 1 et 5."
            break
        fi
    done

    echo "$DateAbsolue, $DateRelative, $NumeroSequence, $tempo_actuel, $touche_pressee" >> "$PathDonnee/InformationExperience.csv"
    echo "Lancement de la sequence suivante"

    compteur=$((compteur + 1))

    if [[ $compteur -eq 10 || $compteur -eq 15 || $compteur -eq 20 ]]; then
        echo ""
        while true; do
            read -p "Êtes-vous motivé à continuer l'expérience et à effectuer encore quelques tâches ? (Oui/Non) : " motivation
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