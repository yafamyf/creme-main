import csv
import fastavro


# Transforme le fichier avro en ficher csv

def avro_to_csv(avro_file_path, csv_file_path):
    # Ouvrir le fichier AVRO
    with open(avro_file_path, 'rb') as avro_file:
        # Lire les enregistrements AVRO
        reader = fastavro.reader(avro_file)
        
        # Ouvrir le fichier CSV pour écrire les données
        with open(csv_file_path, 'w', newline='') as csv_file:
            csv_writer = csv.writer(csv_file)
            
            # Écrire les en-têtes du CSV en utilisant les noms de champs du schéma AVRO
            # On prend les noms de champ du premier enregistrement
            headers = reader.schema['fields']
            csv_writer.writerow([field['name'] for field in headers])
            
            # Lire chaque enregistrement du fichier AVRO et l'écrire dans le fichier CSV
            for record in reader:
                csv_writer.writerow(record.values())


# Exemple d'utilisation
avro_file_path = 'Data/participant_data/2025-01-09/222-3YK3K152R7/raw_data/v6/1-1-222_1736430550.avro'  
# Remplacer par le chemin de le fichier AVRO dans votre dossier
csv_file_path = 'resultat.csv'   # Remplacer par le chemin où tu veux enregistrer le fichier CSV

avro_to_csv(avro_file_path, csv_file_path)