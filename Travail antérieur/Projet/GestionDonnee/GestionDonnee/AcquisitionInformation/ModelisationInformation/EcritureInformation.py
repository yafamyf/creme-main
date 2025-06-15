import csv

def get_participant_info():
    nom = input("Nom: ")
    prenom = input("Prénom: ")
    solfegeEcole = int(input("Connaissance en solfège en ecole: "))
    solfegeLoisir = int(input("Connaissance en solfège en loisir: "))
    age = int(input("Âge début apprentissage: "))
    duree_apprentissage = int(input("Durée apprentissage (en années): "))
    
    # Collecter les informations sur les instruments
    instruments = []
    while True:
        instrument = input("Instrument (ou appuyez sur Entrée pour terminer): ")
        if instrument == "":
            break
        annees_pratique = int(input(f"Nombre d'années de pratique pour {instrument}: "))
        heures_semaine = int(input(f"Nombre d'heures de pratique par semaine pour {instrument}: "))
        instruments.append(f"{instrument}:{annees_pratique}:{heures_semaine}")
    
    instruments_str = ";".join(instruments)
    
    ecoute = int(input("Écoute (1-4): "))
    
    Classique = int(input("Ecoute Classique "))
    Pop = int(input("Ecoute Pop: "))
    Jazz = int(input("Ecoute Jazz: "))
    Rock = int(input("Ecoute Rock: "))
    VarieteFrançaise = int(input("Ecoute Variété française: "))
    MusiqueExperimentale = int(input("Ecoute Musique expérimentale: "))
    Metal = int(input("Ecoute Métal: "))
    MusiqueMonde = int(input("Ecoute Musique du monde: "))
    SoulFunk = int(input("Ecoute Soul/Funk: "))
    Folk = int(input("Ecoute Folk: "))
    HipHop = int(input("Ecoute Hip Hop: "))
    Rap = int(input("Ecoute Rap: "))
    MusiqueElectronique = int(input("Ecoute Musique électronique: "))
    DnB = int(input("Ecoute DnB: "))
    Country = int(input("Ecoute Country: "))
    Reggae = int(input("Ecoute Reggae: "))
    RnB = int(input("Ecoute RnB: "))
    MusiqueIndependante = int(input("Ecoute Musique indépendante: "))

    return [nom, prenom, solfegeEcole, solfegeLoisir, age, duree_apprentissage, instruments_str, ecoute, Classique, 
            Pop, Jazz, Rock, VarieteFrançaise, MusiqueExperimentale, Metal,
            MusiqueMonde, SoulFunk, Folk, HipHop, Rap, MusiqueElectronique,
            DnB, Country, Reggae, RnB, MusiqueIndependante]

def save_to_csv(data, filename):
    header = ["Nom", "Prénom", "Connaissance Solfege Ecole", "Connaissance Solfege Loisir", "Âge début apprentissage", "Durée apprentissage", "Instruments", "Écoute", "Classique", "Pop", "Jazz", "Rock", "Variété française", "Musique expérimentale", "Métal", "Musique du monde", "Soul/Funk", "Folk", "Hip Hop", "Rap", "Musique électronique", "DnB", "Country", "Reggae", "RnB", "Musique indépendante"]
    
    try:
        with open(filename, 'r') as f:
            file_empty = (f.readline() == '')
    except FileNotFoundError:
        file_empty = True

    with open(filename, 'a', newline='') as f:
        writer = csv.writer(f)
        
        if file_empty:
            writer.writerow(header)
        writer.writerow(data)

def main():
    participant_info = get_participant_info()
    save_to_csv(participant_info, "participants.csv")

if __name__ == "__main__":
    main()
