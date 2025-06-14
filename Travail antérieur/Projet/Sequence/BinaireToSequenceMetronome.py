from music21 import stream, note, duration, instrument, tempo, midi
import sys

i = 0
Etape = sys.argv[1]

Signification = {
        "1": "Note",
        "0": "Silence"
}

TempsDouble = 0.25
TempsNoire = 1
Woodblock = instrument.Woodblock()
Tempo = 90

def CreationPartition():
    score = stream.Score()

    # Définir le tempo de la partition
    VitesseTempo = tempo.MetronomeMark(number=Tempo)
    score.insert(0, VitesseTempo)

    # Créer deux voix dans la partition
    voix1 = stream.Part()
    voix2 = stream.Part()

    voix1.insert(0, instrument.Woodblock())
    voix1.insert(0, VitesseTempo)
       
    voix2.insert(0, instrument.Cowbell())
    voix2.insert(0, VitesseTempo)
    
    # Ajouter les voix à la partition principale
    score.append(voix1)
    score.append(voix2)

    return score

def LectureSequence(Part, Sequence):
    cpt = 0

    while cpt < 4:
        n = note.Note(76)
        n.duration = duration.Duration(TempsNoire)
        n.volume.velocity = 0  # Volume de la note
        Part.append(n)
        cpt += 1

    for i in range(2):
        #for j in [39,42,56,60,76]:
            for bit in Sequence:
            
                if bit == "1":
                    # Ajouter une note
                    n = note.Note("C")
                    #n = note.Note(j)

                    n.duration = duration.Duration(TempsDouble)
                    n.volume.velocity = 120  # Volume de la note
            
                    Part.append(n)
                elif bit == "0":
                    r = note.Rest()
                    r.duration = duration.Duration(TempsDouble)
                    Part.append(r)

    return Part

def Metronome(Part):
    cpt = 0
    while cpt < 20:
        n = note.Note(76)
        n.duration = duration.Duration(TempsNoire)
        n.volume.velocity = 140  # Volume de la note
        Part.append(n)
        cpt += 1

    return Part

def CreationSequence(Part, Sequence):
    # Accéder aux voix individuellement
    voix1 = Part.parts[0]  # Première voix
    voix2 = Part.parts[1]  # Deuxième voix

    voix1 = LectureSequence(voix1, Sequence)
    voix2 = Metronome(voix2)

    return Part




if Etape == "1":  #Introduction
    NomFichierEntree = "RythmeBinaireIntroduction.txt"
    NomFichierSortie = "SequenceIntroductionReproduction/"
elif Etape == "2" : #Final
    NomFichierEntree = "RythmeBinaireFinal.txt"
    NomFichierSortie = "SequenceRythme/"


with open(NomFichierEntree, 'r') as file:

    # Lire toutes les lignes du fichier
    lines = file.readlines()
    for line in lines:
        i = i + 1
        print(i)
        print(line[0:-1])
        sequence = line[0:-1]

        Partition = CreationPartition()
        Partition = CreationSequence(Partition, sequence)

        midi_filename = NomFichierSortie +"SequenceNumero" + str(i) + ".mid"

        Partition.write('midi', midi_filename)


exit(0)
