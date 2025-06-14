"""
Utilitaire de récupération des données Empatica S3
--------------------------------------------------

Prérequis :

    # Installation des dépendances
    sudo apt update && sudo apt install awscli
    pip install boto3 pandas fastavro

    # Configuration des identifiants Empatica
    aws configure
        AWS Access Key ID     : <votre clé>
        AWS Secret Access Key : <votre secret>
        Default region name   : us-east-1

Le script liste les fichiers disponibles sous v2/1605/ dans le bucket
puis montre un exemple de téléchargement + lecture CSV.

⚠️  Les clés *ne doivent jamais* être ajoutées dans le code !
"""

import os
import boto3
import pandas as pd
from botocore.exceptions import NoCredentialsError

# Paramètres Empatica
S3_BUCKET = "empatica-us-east-1-prod-data"
PREFIX    = "v2/1605/"

# Création du client S3 — les creds sont pris dans ~/.aws/credentials
s3 = boto3.client("s3")


def list_files(prefix: str = PREFIX) -> None:
    """Affiche la liste des fichiers sous le préfixe donné."""
    try:
        paginator = s3.get_paginator("list_objects_v2")
        for page in paginator.paginate(Bucket=S3_BUCKET, Prefix=prefix):
            for obj in page.get("Contents", []):
                print(f"{obj['Key']} — {obj['LastModified']}")
    except NoCredentialsError:
        print(
            "❌  Identifiants AWS manquants ou incorrects. "
            "Exécutez `aws configure` ou définissez les variables d’environnement."
        )


def download_file(key: str, local_path: str) -> None:
    """Télécharge le fichier S3 <key> vers <local_path>."""
    try:
        os.makedirs(os.path.dirname(local_path), exist_ok=True)
        s3.download_file(S3_BUCKET, key, local_path)
        print(f" {key} téléchargé → {local_path}")
    except Exception as e:
        print(f"  Erreur lors du téléchargement : {e}")


if __name__ == "__main__":
    # 1) Liste des fichiers disponibles
    print("=== Contenu du dossier Empatica ===")
    list_files()

    # 2) Exemple de téléchargement d'un fichier précis
    FILE_KEY   = f"{PREFIX}1/1/your_file.csv"      # <-- à adapter
    LOCAL_PATH = "data/your_file.csv"

    download_file(FILE_KEY, LOCAL_PATH)

    # 3) Lecture éventuelle du CSV avec pandas
    if os.path.isfile(LOCAL_PATH):
        df = pd.read_csv(LOCAL_PATH)
        print("\nAperçu du fichier téléchargé :")
        print(df.head())
