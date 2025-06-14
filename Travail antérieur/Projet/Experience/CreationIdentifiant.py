import hashlib
import datetime

fichier = "../GestionDonnee/CorrespondanceIdNom.csv"

def saisir_informations_participant():
    nom_prenom = input()

    # Séparation du nom et du prénom en fonction de l'espace
    if nom_prenom:
        try:
            nom, prenom = nom_prenom.split(' ', 1)
            return nom, prenom
        except ValueError:
            print("Erreur : veuillez entrer à la fois le nom et le prénom séparés par un espace.")
            return None, None
    else:
        print("Aucune information saisie.")
        return None, None

def generer_identifiant_unique(nom, prenom, date_naissance):
    # Concaténation des informations du participant
    infos_participant = nom + prenom + date_naissance
    
    # Génération de l'empreinte SHA-256
    empreinte_sha256 = hashlib.sha256(infos_participant.encode()).hexdigest()
    
    return empreinte_sha256

def main():
    # Exemple d'utilisation
    Nom, Prenom = saisir_informations_participant()
    while (Nom == None or Prenom == None):
        Nom, Prenom = saisir_informations_participant()

    # Obtenir la date actuelle
    Time = datetime.datetime.now()
    Date = "{}{}{}".format(Time.day,Time.month,Time.year)

    identifiant_unique = generer_identifiant_unique(Nom, Prenom, Date)

    Information = "{},{},{},{}".format(Nom, Prenom, Date, identifiant_unique)

    with open(fichier, 'a') as f:
        print(Information, file=f)  
   
    return identifiant_unique

if __name__ == "__main__":
    identifiant = main()
    print(identifiant)
