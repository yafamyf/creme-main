#!/bin/bash


#9 = pc / ecouteur, 10 = enceinte Florence
# Enceinte=9
# Enceinte=10
Enceinte=0 # enceinte virtuelle blackhole loopback pour Florence

echo "Entrez le nom et le prénom du participant : "

#fichier="Alan-Menet"
fichier=$(python CreationIdentifiant.py)

echo $fichier


# Faire la selection des taches ici
Tache=$((RANDOM % 2 + 1))
echo $Tache

if [[ $Tache = 1 ]]; then
    echo ""
    echo "Experience Perception selectionnee"
    echo "En route pour l'introduction Perception."

    sleep 1
    while true; do
        read -n 1 -s -r -p "Appuyer sur un chiffre pour continuer... " touche_pressee
        if [[ $touche_pressee =~ ^[0-9]$ ]]; then
            break
        fi
    done
    ./ProtocoleIntroductionSequence.sh "$fichier" "$Enceinte"
    
    echo ""
    echo "Fin de l'introduction."
    echo "Commencons les vraies sequences."

    sleep 2
    while true; do
        read -n 1 -s -r -p "Appuyer sur un chiffre pour continuer... " touche_pressee
        if [[ $touche_pressee =~ ^[0-9]$ ]]; then
            break
        fi
    done
    ./ProtocolePulsationSequence.sh "$fichier" "$Enceinte"

    echo ""
    echo "Fin des sequences perception."
    echo "Debut des sequences d'introduction de Reproduction."
    sleep 2
    while true; do
        read -n 1 -s -r -p "Appuyer sur un chiffre pour continuer... " touche_pressee
        if [[ $touche_pressee =~ ^[0-9]$ ]]; then
            break
        fi
    done


    sleep 2
    ./ProtocoleIntroductionSequenceReproduction.sh "$fichier" "$Enceinte"

    echo ""
    echo "Fin de l'introduction, debut de l'experience"
    while true; do
        read -n 1 -s -r -p "Appuyer sur un chiffre pour continuer... " touche_pressee
        if [[ $touche_pressee =~ ^[0-9]$ ]]; then
            break
        fi
    done

    ./ProtocoleReproductionSequence.sh "$fichier" "$Enceinte"
    echo ""
    echo "Fin de lexperience."
    sleep 2



else
    echo ""
    echo "Experience Reproduction selectionnee"
    echo "En route pour l'introduction Reproduction."

    sleep 1
    while true; do
        read -n 1 -s -r -p "Appuyer sur un chiffre pour continuer... " touche_pressee
        if [[ $touche_pressee =~ ^[0-9]$ ]]; then
            break
        fi
    done
    ./ProtocoleIntroductionSequenceReproduction.sh "$fichier" "$Enceinte"
    
    echo ""
    echo "Fin de l'introduction."
    echo "Commencons les vraies sequences."

    sleep 2
    while true; do
        read -n 1 -s -r -p "Appuyer sur un chiffre pour continuer... " touche_pressee
        if [[ $touche_pressee =~ ^[0-9]$ ]]; then
            break
        fi
    done
    ./ProtocoleReproductionSequence.sh "$fichier" "$Enceinte"

    echo ""
    echo "Fin des sequences Reproduction."
    echo "Debut des sequences d'introduction de Perception."
    sleep 2
    while true; do
        read -n 1 -s -r -p "Appuyer sur un chiffre pour continuer... " touche_pressee
        if [[ $touche_pressee =~ ^[0-9]$ ]]; then
            break
        fi
    done


    sleep 2
    ./ProtocoleIntroductionSequence.sh "$fichier" "$Enceinte"
    echo ""
    echo "Fin de l'introduction, debut de l'experience"
    while true; do
        read -n 1 -s -r -p "Appuyer sur un chiffre pour continuer... " touche_pressee
        if [[ $touche_pressee =~ ^[0-9]$ ]]; then
            break
        fi
    done

    ./ProtocolePulsationSequence.sh "$fichier" "$Enceinte"

    echo ""
    echo "Fin de l'experience."
    sleep 2
fi

