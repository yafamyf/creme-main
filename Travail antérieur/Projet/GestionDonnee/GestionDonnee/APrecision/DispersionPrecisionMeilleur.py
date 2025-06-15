import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats

from collections import Counter
import csv
import os


# Fonction pour lire le fichier CSV et stocker les timestamps dans une liste
def read_timestamps_from_csv(file_path):
    timestamps_participants = []
    with open(file_path, 'r') as file:
        csv_reader = csv.reader(file)
        for row in csv_reader:
            # Ignorer la première et la dernière valeur (supposé identifiants ou autres colonnes non utiles)
            row = row[1:-1]
            # Convertir chaque valeur de chaîne dans la ligne en un flottant
            timestamps = [float(ts) for ts in row]
            timestamps_participants.append(timestamps)
    return timestamps_participants


# Fonction pour soustraire la première valeur des timings réels de chaque timing expérimental
def subtract_first_value(experiment_timings, real_timings):
    differences = []
    for exp, real in zip(experiment_timings, real_timings):
        if real:  # Assurez-vous que la liste n'est pas vide
            first_real = real[0]
            differences.append([t - first_real for t in exp])
    return differences


def identify_tempos(timestamps_reelle):
    # Calculer les différences entre les timestamps réels pour chaque participant
    tempos = []
    for timestamps in timestamps_reelle:
        differences = np.diff(timestamps)
        tempos.extend(differences)
    
    # Trouver les trois valeurs les plus fréquentes (les tempos)
    most_common_tempos = [tempo for tempo, _ in Counter(tempos).most_common(3)]
    return most_common_tempos

def get_multiples(tempos, max_multiples=15):
    multiples = []
    for tempo in tempos:
        tempo_multiples = [tempo * i for i in range(1, max_multiples + 1)]
        multiples.append(tempo_multiples)
    return multiples


def separate_by_tempo(adjusted_timings, timestamps_reelle, tempos):
    separated_timings = {tempo: [] for tempo in tempos}
    
    for i, timings in enumerate(adjusted_timings):
        # Calculer les différences pour chaque participant
        differences = np.diff(timestamps_reelle[i])
        
        # Associer les ajustements aux tempos
        for timing in timings:
            for tempo in tempos:
                if any(np.isclose(d, tempo, atol=0.01) for d in differences):
                    separated_timings[tempo].append(timing)
                    break  # Sortir dès qu'on trouve une correspondance
    
    return separated_timings



# Affichage des résultats pour vérification
"""for i, timing in enumerate(differences):
    print(f"Sequence {i+1}: {timing}")
"""

# Fonction pour créer des graphes pour les tempos différents
def plot_tempos(separated_timings, vertical_lines):
    # Créer une figure avec trois sous-graphiques
    fig, axes = plt.subplots(nrows=3, ncols=1, figsize=(10, 6), sharex=True)

    colors = ['blue', 'green', 'red']
    styles = ['o', 's', '^']

    for i, (tempo, timings) in enumerate(separated_timings.items()):
        # Filtrer les valeurs négatives
        filtered_timings = [t for t in timings if t >= 0]
        filtered_offsets = [0] * len(filtered_timings)
        
        ax = axes[i]
        ax.scatter(filtered_timings, filtered_offsets, color=colors[i % len(colors)], marker=styles[i % len(styles)])
        ax.set_title(f'Tempo : {int(round(60/tempo))} battements par minute. ({tempo:.3f} secondes entre deux notes)')
        ax.set_xlabel('Temps (seconds)')
        ax.grid(False)

        for line in vertical_lines[i]:
            ax.axvline(x=line, color='grey', linestyle='-',linewidth=0.5)
    
    plt.tight_layout()
    plt.show()




folder_path = '../Perception/'

i=0
# Parcourir le dossier et lire les fichiers CSV
for dossier in os.listdir(folder_path):
    Chemin = os.path.join(folder_path, dossier)
    i=i+1
    #print(Chemin)
    if Chemin == "../Perception/2c90c744d2ce7b6f385dc87d949fe3faa2f752713c94bad9fbc4cbb5f31f66b1":
    #print(dossier)
        for fichier in os.listdir(Chemin):
        

            #print(fichier)
            # Lire les timestamps
            timestamps_reelle = read_timestamps_from_csv(Chemin+"/CalculPulseReelle.txt")
            timestamps_Participant = read_timestamps_from_csv(Chemin+"/RetranscriptionInput.txt")



            differences = subtract_first_value(timestamps_Participant, timestamps_reelle)

            # Exemple d'utilisation
            tempos = identify_tempos(timestamps_reelle)

            multiples = get_multiples(tempos)

            # Exemple d'utilisation
            separated_timings = separate_by_tempo(differences, timestamps_reelle, tempos)
            #print("Separated timings:", separated_timings)

            # Créer des graphes pour les tempos différents
            plot_tempos(separated_timings, multiples)

            #plt.savefig("Perception/DispersionPrecision/"+dossier+str(i)+'.png')
            #plt.savefig("Perception/DispersionPrecision/"+dossier+'test.png')

            plt.savefig("test/"+dossier+'test.png')

