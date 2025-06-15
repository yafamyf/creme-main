import numpy as np
import matplotlib.pyplot as plt
import csv
import os


# Fonction pour lire les timestamps depuis un fichier CSV
def read_timestamps_from_csv(file_path):
    timestamps = []
    with open(file_path, 'r') as file:
        csv_reader = csv.reader(file)
        for row in csv_reader:
            # Ignorer la première et dernière valeur (si besoin)
            row = row[1:-1]
            timestamps.append([float(ts) for ts in row])
    return timestamps


# Fonction pour lire les informations des séquences depuis InformationExperience.csv
def read_sequence_info(file_path):
    sequence_info = []
    with open(file_path, 'r') as file:
        csv_reader = csv.reader(file)
        next(csv_reader)  # Sauter l'entête
        for row in csv_reader:
            sequence_number = int(row[2])  # Colonne "NumeroSequence"
            sequence_info.append((sequence_number, row))  # Associer le numéro de séquence à la ligne
    return sequence_info


# Fonction pour soustraire la première valeur des timings réels de chaque timing expérimental
def subtract_first_value(experiment_timings, real_timings):
    differences = []
    for exp, real in zip(experiment_timings, real_timings):
        if real:  # Vérifier que la liste n'est pas vide
            first_real = real[0]
            differences.append([t - first_real for t in exp])
    return differences


# Fonction pour séparer les timings par séquence
def separate_by_sequence(adjusted_timings, num_sequences):
    separated_timings = {}
    for i in range(num_sequences):
        # Assurer que la clé de séquence commence à 1 et correspond aux numéros de séquences
        if i + 1 < len(adjusted_timings):
            separated_timings[i + 1] = adjusted_timings[i]
    return separated_timings


# Fonction pour tracer les graphiques avec les titres des séquences
def plot_all_sequences_with_titles(separated_timings, real_timestamps, sequence_titles, output_file=None):
    num_sequences = len(separated_timings)
    fig, axes = plt.subplots(nrows=num_sequences, ncols=1, figsize=(10, num_sequences * 2), sharex=True)

    if num_sequences == 1:
        axes = [axes]  # S'assurer que `axes` est une liste même pour un seul graphique

    for i, (seq, timings) in enumerate(separated_timings.items()):
        ax = axes[i]
        filtered_timings = [t for t in timings if t >= 0]
        filtered_offsets = [0] * len(filtered_timings)

        # Tracer les points des timings
        ax.scatter(filtered_timings, filtered_offsets, color='blue', marker='o')
        ax.set_title(f'Séquence {seq}')  # Utiliser le numéro de séquence comme titre
        ax.set_ylabel('Offset')
        ax.grid(False)

        # Ajouter des lignes verticales pour les tempos associés
        if i < len(real_timestamps):
            differences = np.diff(real_timestamps[i])
            for tempo in differences:
                tempo_multiples = [tempo * j for j in range(1, 16)]
                for line in tempo_multiples:
                    ax.axvline(x=line, color='grey', linestyle='-', linewidth=0.5)

    axes[-1].set_xlabel('Temps (seconds)')  # Ajouter un label X sur le dernier sous-graphe
    plt.tight_layout()

    if output_file:
        plt.savefig(output_file)  # Sauvegarder dans un fichier si un chemin est donné
        plt.close(fig)
    else:
        plt.show()


# Pipeline principal pour traiter les fichiers
folder_path = '../Perception/'

for dossier in os.listdir(folder_path):
    chemin_dossier = os.path.join(folder_path, dossier)
    
    if os.path.isdir(chemin_dossier):
        # Lire les fichiers nécessaires pour chaque participant
        timestamps_reelle = read_timestamps_from_csv(os.path.join(chemin_dossier, "CalculPulseReelle.txt"))
        timestamps_participant = read_timestamps_from_csv(os.path.join(chemin_dossier, "RetranscriptionInput.txt"))
        sequence_titles = read_sequence_info(os.path.join(chemin_dossier, "InformationExperience.csv"))

        # Trier les séquences par numéro de séquence
        sequence_titles.sort(key=lambda x: x[0])  # Trier par le premier élément (le numéro de séquence)

        # Calculer les différences et séparer par séquence
        differences = subtract_first_value(timestamps_participant, timestamps_reelle)
        num_sequences = len(timestamps_reelle)  # Nombre de séquences basées sur les lignes de timestamps réels
        separated_timings = separate_by_sequence(differences, num_sequences)

        # Trier les timings séparés par séquence pour garantir l'ordre
        separated_timings_sorted = {seq: separated_timings[seq] for seq, _ in sequence_titles if seq in separated_timings}

        # Générer un nom de fichier unique pour le participant
        participant_id = os.path.basename(dossier)  # Nom du dossier utilisé comme identifiant
        output_file = f"DispersionSequenceTriee/participant_{participant_id}_sequences.png"

        # Tracer les graphiques
        plot_all_sequences_with_titles(separated_timings_sorted, timestamps_reelle, sequence_titles, output_file=output_file)
