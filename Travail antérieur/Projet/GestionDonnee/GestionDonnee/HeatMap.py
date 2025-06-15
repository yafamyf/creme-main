import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import spearmanr

# Valeur de complexite suivant les differentes metriques
ClockBeat = [1,0,5,7,3,7,8,4,11,9,9,7,5,5,1,3,3,5,5,11,9,1,11,9,3,15]
Pressing = [8,10,10.5,10.5,7,12,11.5,15.5,16,13.5,12.5,13.5,12.5,10.5,17.5,15.5,17,19,14.5,23.5,19.5,17,20,20,18,8]
Toussaint = [25,23,22,28,23,23,22,22,23,22,22,22,22,22,20,20,19,19,21,17,19,19,18,18,20,9]

PercepionMusicien = [2.25,2.66,1.85,2.83,2.0,1.66,1.75,2.83,2.0,2.0,1.66,1.33,1.33,2.0,3.0,2.83,2.0,2.0,2.66,3.16,3.0,2.5,3.28,2.5,1.5,2.5]
PercepionNonMusicien = [3.5,2.6,3.14,3.0,2.66,4.5,3.0,3.75,4.0,3.66,3.33,2.6,2.57,2.0,4.0,3.0,2.5,2.75,2.5,3.42,3.0,3.0,3.0,2.5,2.66,2.6]

ReproductionMusicien = [2.0,2.33,3.4,3.13,3.06,2.53,2.93,3.0,2.66,2.73,2.93,2.46,2.2,2.46,2.86,2.4,2.73,3.06,3.4,3.2,3.73,3.4,3.13,3.26,3.33,3.4]
ReproductionNonMusicien = [2.75,2.75,3.75,2.75,3.92,3.66,3.0,2.83,3.66,3.5,3.33,3.15,2.83,2.16,3.5,2.75,2.75,3.0,3.41,3.83,4.0,3.83,3.83,3.5,3.58,3.75]

# Calcul des corrélations (Spearman)
corr_methode1_2, _ = spearmanr(ClockBeat, Pressing)
corr_methode1_3, _ = spearmanr(ClockBeat, Toussaint)
corr_methode1_4, _ = spearmanr(ClockBeat, PercepionMusicien)
corr_methode1_5, _ = spearmanr(ClockBeat, PercepionNonMusicien)
corr_methode1_6, _ = spearmanr(ClockBeat, ReproductionMusicien)
corr_methode1_7, _ = spearmanr(ClockBeat, ReproductionNonMusicien)

corr_methode2_3, _ = spearmanr(Pressing, Toussaint)
corr_methode2_4, _ = spearmanr(Pressing, PercepionMusicien)
corr_methode2_5, _ = spearmanr(Pressing, PercepionNonMusicien)
corr_methode2_6, _ = spearmanr(Pressing, ReproductionMusicien)
corr_methode2_7, _ = spearmanr(Pressing, ReproductionNonMusicien)

corr_methode3_4, _ = spearmanr(Toussaint, PercepionMusicien)
corr_methode3_5, _ = spearmanr(Toussaint, PercepionNonMusicien)
corr_methode3_6, _ = spearmanr(Toussaint, ReproductionMusicien)
corr_methode3_7, _ = spearmanr(Toussaint, ReproductionNonMusicien)

corr_methode4_5, _ = spearmanr(PercepionMusicien, PercepionNonMusicien)
corr_methode4_6, _ = spearmanr(PercepionMusicien, ReproductionMusicien)
corr_methode4_7, _ = spearmanr(PercepionMusicien, ReproductionNonMusicien)

corr_methode5_6, _ = spearmanr(PercepionNonMusicien, ReproductionMusicien)
corr_methode5_7, _ = spearmanr(PercepionNonMusicien, ReproductionNonMusicien)

corr_methode6_7, _ = spearmanr(ReproductionMusicien, ReproductionNonMusicien)


# Création d'une matrice de corrélation
correlation_matrix = np.array([
    [1.0, corr_methode1_2, corr_methode1_3, corr_methode1_4, corr_methode1_5, corr_methode1_6, corr_methode1_7],
    [corr_methode1_2, 1.0, corr_methode2_3, corr_methode2_4, corr_methode2_5, corr_methode2_6, corr_methode2_7],
    [corr_methode1_3, corr_methode2_3, 1.0, corr_methode3_4, corr_methode3_5, corr_methode3_6, corr_methode3_7],
    [corr_methode1_4, corr_methode2_4, corr_methode3_4, 1.0, corr_methode4_5, corr_methode4_6, corr_methode4_7],
    [corr_methode1_5, corr_methode2_5, corr_methode3_5, corr_methode4_5, 1.0, corr_methode5_6, corr_methode5_7],
    [corr_methode1_6, corr_methode2_6, corr_methode3_6, corr_methode4_6, corr_methode5_6, 1.0, corr_methode6_7],
    [corr_methode1_7, corr_methode2_7, corr_methode3_7, corr_methode4_7, corr_methode5_7, corr_methode6_7, 1.0]
])

# Création d'un DataFrame pour l'affichage
df_corr = pd.DataFrame(correlation_matrix, index=["ClockBeat Essens", "Cognitive Pressing", "Metrical Toussaint", "PercepionMusicien", "PercepionNonMusicien", "ReproductionMusicien", "ReproductionNonMusicien"], columns=["ClockBeat Essens", "Cognitive Pressing", "Metrical Toussaint", "PercepionMusicien", "PercepionNonMusicien", "ReproductionMusicien", "ReproductionNonMusicien"])


# Création du heatmap avec matplotlib
fig, ax = plt.subplots()
cax = ax.matshow(correlation_matrix, cmap='coolwarm')

# Ajouter une barre de couleur
fig.colorbar(cax)

# Ajouter les labels
ax.set_xticks(np.arange(len(correlation_matrix)))
ax.set_yticks(np.arange(len(correlation_matrix)))
ax.set_xticklabels(["ClockBeat Essens", "Cognitive Pressing", "Metrical Toussaint", "PercepionMusicien", "PercepionNonMusicien", "ReproductionMusicien", "ReproductionNonMusicien"])
ax.set_yticklabels(["ClockBeat Essens", "Cognitive Pressing", "Metrical Toussaint", "PercepionMusicien", "PercepionNonMusicien", "ReproductionMusicien", "ReproductionNonMusicien"])

# Afficher les valeurs dans les cellules
for (i, j), val in np.ndenumerate(correlation_matrix):
    ax.text(j, i, f'{val:.2f}', ha='center', va='center', color='black')

plt.title('Heatmap des corrélations entre les méthodes')

plt.savefig('heatmap.png')


plt.show(block=True)

print("check")