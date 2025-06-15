# Ouvrir le fichier en mode lecture
with open('fichier_combine.csv', 'r') as f:
    # Lire chaque ligne du fichier
    lines = f.readlines()

# Séparer chaque ligne en utilisant la virgule comme séparateur et prendre la première partie
cleaned_lines = [line.split(',')[0] for line in lines]

# Joindre les lignes nettoyées en une seule chaîne de caractères
cleaned_content = '\n'.join(cleaned_lines)

# Écrire le contenu nettoyé dans un nouveau fichier
with open('fichier_nettoye.csv', 'w') as f:
    f.write(cleaned_content)
