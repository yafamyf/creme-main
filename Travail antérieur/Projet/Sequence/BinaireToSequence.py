from music21 import stream, note, duration, instrument, tempo, midi
import sys



i = 0
Etape = sys.argv[1]
Tempo = sys.argv[2]
#Tempo = 70


Signification = {
        "1": "Note",
        "0": "Silence"
}

TempsDouble = 0.25
Woodblock = instrument.Woodblock()


def CreationPartition():
    part = stream.Part()
    part.insert(0, Woodblock)
    
    part.insert(0, tempo.MetronomeMark(number=Tempo))    
    return part


def LectureSequence(Part, Sequence):
    
    for bit in Sequence:
        if bit == "1":
            # Ajouter une note
            n = note.Note("C4")

            n.duration = duration.Duration(TempsDouble)
            n.volume.velocity = 120  # Volume de la note
    
            Part.append(n)
        elif bit == "0":
            r = note.Rest()
            r.duration = duration.Duration(TempsDouble)
            Part.append(r)

    return Part
        


def CreationSequence(Part, Sequence, NomFichierSortie, i):

    LectureSequence(Part, Sequence)

    # Créer une mesure pour contenir les notes et les pauses
    measure = stream.Measure()
    measure.append(Part)

    # Ajouter la mesure à une partition
    score = stream.Score()
    #score.append(measure)
    score.repeatAppend(measure, 4)  
    midi_filename = NomFichierSortie + str(Tempo) + "/SequenceNumero" + str(i) + ".mid"


    score.write('midi', midi_filename)



def EcritureSequenceFichier(NomFichierEntree, NomFichierSortie, i):
    # Ouvrir le fichier en mode lecture
    with open(NomFichierEntree, 'r') as file:


        # Lire toutes les lignes du fichier
        lines = file.readlines()
        for line in lines:

            i = i+1
            print(i)
            print(line[0:-1])
            sequence = line[0:-1]

            Partition = CreationPartition()
            CreationSequence(Partition, sequence, NomFichierSortie, i)


if Etape == "1":  #Introduction
    NomFichierEntree = "RythmeBinaireIntroduction.txt"
    NomFichierSortie = "SequenceIntroductionPerception/"
elif Etape == "2" : #Final
    NomFichierEntree = "RythmeBinaireFinal.txt"
    NomFichierSortie = "SequencePulse/"

EcritureSequenceFichier(NomFichierEntree, NomFichierSortie, i)

print("Ecriture reussis")

exit(0)

