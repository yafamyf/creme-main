import pandas as pd
import numpy as np

# Lire les fichiers CSV sans en-tête


file1 = 'cdc41cb854d0d063358cb00855f1f017a57e63ca94a4bb81db4047db6da15aca/EDA1.csv'
file2 = 'cdc41cb854d0d063358cb00855f1f017a57e63ca94a4bb81db4047db6da15aca/EDA2.csv'

# Lire les fichiers CSV en spécifiant que la première ligne ne contient pas d'en-tête
df1 = pd.read_csv(file1, header=None)
df2 = pd.read_csv(file2, header=None)

# Extraire les valeurs de début de temps et de fréquence
timestamp_start1 = df1.iloc[0, 0]  # Première valeur de la première colonne
timestamp_start2 = df2.iloc[0, 0]  
freq1 = df1.iloc[1, 0]  # Deuxième valeur de la première colonne
freq2 = df2.iloc[1, 0]  

# Supprimer les deux premières lignes (timestamp de début et fréquence d'enregistrement)
Tempo = df1.iloc[:2]
df1 = df1.iloc[2:]
df2 = df2.iloc[2:]

# Créer une colonne de temps pour chaque fichier
df1['Time'] = df1.index * (1 / freq1) + timestamp_start1
df2['Time'] = df2.index * (1 / freq2) + timestamp_start2

# Déterminer l'écart de temps entre les deux fichiers
time_gap = timestamp_start2 - df1['Time'].iloc[-1]

# Créer un DataFrame pour les valeurs à zéro
if time_gap > 0:
    zero_data = np.zeros((int(time_gap * freq1), df1.shape[1]))
    df_zero = pd.DataFrame(zero_data)
    df_zero['Time'] = df1['Time'].iloc[-1] + np.arange(1, len(df_zero) + 1) * (1 / freq1)
else:
    df_zero = pd.DataFrame()

# Ajouter les colonnes manquantes pour le DataFrame à zéro
for col in df1.columns:
    if col not in df_zero.columns:
        df_zero[col] = np.nan

# Concaténer les DataFrames
combined_df = pd.concat([df1, df_zero, df2], ignore_index=True)

# Sauvegarder le DataFrame combiné dans un nouveau fichier CSV
combined_df.to_csv('fichier_combine.csv', index=False, header=False)
