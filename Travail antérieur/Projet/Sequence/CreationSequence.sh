
echo Creation Dossier

PathIntro1="./SequenceIntroductionPerception/"
PathIntro2="./SequenceIntroductionReproduction/"

if [ -d "$PathIntro1" ]; then
    echo "Le dossier existe déjà, creation des sequences"
else
    echo "Creation du dossier."
    mkdir -p "$PathIntro1"
    mkdir -p "$PathIntro1""70"
    mkdir -p "$PathIntro1""90"
    mkdir -p "$PathIntro1""110"
fi


if [ -d "$PathIntro2" ]; then
    echo "Le dossier existe déjà, creation des sequences"
else
    echo "Creation du dossier."
    mkdir -p "$PathIntro2"
fi

echo creation dossier final

PathPerception="./SequencePulse/"
PathReproduction="./SequenceRythme/"


if [ -d "$PathPerception" ]; then
    echo "Le dossier existe déjà, creation des sequences"
else
    echo "Creation du dossier."
    mkdir -p "$PathPerception"
    mkdir -p "$PathPerception""70"
    mkdir -p "$PathPerception""90"
    mkdir -p "$PathPerception""110"
fi


if [ -d "$PathReproduction" ]; then
    echo "Le dossier existe déjà, creation des sequences"
else
    echo "Creation du dossier."
    mkdir -p "$PathReproduction"
fi


echo debut creation sequence

#arg 1 = intro / final
#arg 2 = tempo
for Etape in 1 2
do
    echo Perception
    for Tempo in 70 90 110
    do
        fichier=$(python BinaireToSequence.py $Etape $Tempo)
    done

    echo Reproduction
    fichier=$(python BinaireToSequenceMetronome.py $Etape)

    echo Etape $Etape fini
done
