import sys
import os


ListeNumeroSequence = []
TempoAssocie = []
ComplexiteAssocie = []


#ChatGPT
def write_to_csv(IdentifiantParticipant, sequence_sorted, Tempo_sorted, notes_sorted, filename):
    header = "IDParticpant,NumeroSequence,TempoAssocie,NoteAssocie"
    file_exists = os.path.exists(filename)

    with open(filename, 'a') as f:
        # Vérifiez si le fichier est vide
        if not file_exists or os.stat(filename).st_size == 0:
            # Le fichier est vide, écrire l'en-tête
            f.write(header + "\n")

        # Écriture des données
        for i in range(len(sequence_sorted)):
            f.write("{},{},{},{}\n".format(IdentifiantParticipant, int(sequence_sorted[i]), int(Tempo_sorted[i]), int(notes_sorted[i])))

# Fin GPT


if len(sys.argv) == 4:

    IdentifiantParticipant = sys.argv[1]
    FichierEntree = sys.argv[2]
    NomFichierSortie = sys.argv[3]

    # Ouvrir le fichier en mode lecture
    with open(FichierEntree, 'r') as file:
        next(file) 
        for ligne in file:
            # Séparation de la ligne en fonction de la virgule
            colonne = ligne.split(',')
            # Extraction du troisième élément (indice 2 car l'index commence à 0)
            NumeroSequence=int(colonne[2].strip())
            ListeNumeroSequence.append(NumeroSequence)

            Tempo=int(colonne[3].strip())
            TempoAssocie.append(Tempo)

            NoteComplexite=int(colonne[4].strip())
            ComplexiteAssocie.append(NoteComplexite)


    # Combiner les deux listes en une liste de tuples
    combined_list = list(zip(ListeNumeroSequence, TempoAssocie, ComplexiteAssocie))

    # Trier la liste combinée en fonction de la première liste (sequence)
    combined_sorted = sorted(combined_list, key=lambda x: x[0])

    # Séparer la liste combinée triée en deux listes distinctes
    Sequence_sorted, Tempo_sorted, Notes_sorted = zip(*combined_sorted)

    # Convertir les tuples en listes
    Sequence_sorted = list(Sequence_sorted)
    Tempo_sorted = list(Tempo_sorted)
    Notes_sorted = list(Notes_sorted)


    write_to_csv(IdentifiantParticipant, Sequence_sorted, Tempo_sorted, Notes_sorted, NomFichierSortie)


