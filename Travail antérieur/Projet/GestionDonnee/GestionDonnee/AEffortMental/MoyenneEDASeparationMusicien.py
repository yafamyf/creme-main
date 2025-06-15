import os
import sys
import csv
import numpy as np
import neurokit2 as nk
from scipy import stats, integrate
import pandas as pd


# Fonction pour identifier si un participant est musicien ou non
def EstMusicien(identifiant): 
    df = pd.read_csv("../AcquisitionInformation/ModelisationInformation/participants.csv")
    ligne = df[df['Identifiant'] == identifiant]
    if not ligne.empty:
        connaissance_ecole = ligne['Connaissance Solfege Ecole'].values[0]
        connaissance_loisir = ligne['Connaissance Solfege Loisir'].values[0]
        if connaissance_ecole == 1 or connaissance_loisir == 1:
            return 1  # Musicien
        else:
            return 2  # Non-musicien
    return None  # Si l'identifiant n'est pas trouvé


def RecuperationMatrice(CheminParticipant,Duree):
    ListeTimeDebut = []
    ListeTimeFin = []
    ListeNumeroSequence = []
    ListeComplexite = []
    ListeTempo = []

    if Duree == 1:
        DureeExperience = 20
    elif Duree == 2:
        DureeExperience = 40

    # Ouverture du fichier CSV et lecture des lignes
    with open(CheminParticipant, mode='r') as file:
        csv_reader = csv.reader(file)
        next(csv_reader)
        for row in csv_reader:
            Time, Heure, NumeroSequence, Tempo, Complexite = row
            ListeTimeDebut.append((float(Time)))
            Temps = float((DureeExperience * 60 / int(Tempo)))
            TimeFin = float(Time)+Temps
            ListeTimeFin.append((TimeFin))
            ListeNumeroSequence.append(int(NumeroSequence))
            ListeTempo.append(int(Tempo))
            ListeComplexite.append(int(Complexite))
        


    return ListeTimeDebut, ListeTimeFin, ListeNumeroSequence, ListeComplexite, ListeTempo



def traiter_fichier(CheminParticipant, CheminDonneesEDA, PerceptionReproduciton, data):
    if not os.path.exists(CheminParticipant):
        print(f"Fichier manquant : {CheminParticipant}")
        return data
    
    if not os.path.exists(CheminDonneesEDA):
        print(f"Fichier manquant : {CheminDonneesEDA}")
        return data


    DecallageExclusion = 2
    TimeDebut, TimeFin, NumSeq, Complex, Tempo = RecuperationMatrice(CheminParticipant, PerceptionReproduciton)

    ListeComplexiteTheorique = [3.1,3.2,3.1,2.6,2.8,2.5,2.4,3.2,2.4,2.12,2.08,1.80,2.44,3.00,2.04,2.60,3.08,2.56,2.56,2.84,3.60,3.28,3.52,3.60,2.88,4,4]
    """
    for i in range(len(NumSeq)):
        print(i)
        print(NumSeq[i])
        print(ListeComplexiteTheorique[NumSeq[i]-1])
        print(Complex[i])
    """
    # Debut Analyse EDA

    samplingRate = 8


    # Ouvrir le fichier en mode lecture
    with open(CheminDonneesEDA, 'r') as file:
        # Lire toutes les lignes du fichier
        lines = file.readlines()
        # Supprimer les sauts de ligne de chaque ligne et stocker dans une liste
        lines_list = [line.strip() for line in lines]


    TimeStamp=float(lines_list[0])
    Frequence=float(lines_list[1])

    matriceTime = np.array([[TimeStamp,Frequence],
                        [0,0]])


    for i in range(2, len(lines_list)):
        temps_ajuste = TimeStamp + (i - 1) / Frequence
        valeurs = lines_list[i]  # Récupérer les valeurs à partir de la troisième colonne
        NouvelleLigne = [temps_ajuste,valeurs]
        matriceTime = np.insert(matriceTime, -1, NouvelleLigne, axis=0)

    matriceTime = np.delete(matriceTime, -1, axis=0)

    # matriceTime correspond a la valeur de chaque EDA suivant le temps



    i=0
    ListeTempo=[]

    print(np.shape(TimeDebut))

    for TimeEDA in matriceTime:
        #Si je ne suis pas arrivé à la derniere sequence
        if (i < np.shape(TimeDebut)[0] and 
        #Je prend le temps debut de ma sequence + une constante
        TimeEDA[0] >= (TimeDebut[i]+DecallageExclusion) and
        #Je vais jusque la fin de la sequence (faut que je la calcule via le tempo) 
        # - constance, (ca a l'air beaucoup, ptet reduire c et modifier en +2*c et -c plus tard)
        TimeEDA[0] <= TimeFin[i]-(DecallageExclusion-1)):

            ListeTempo.append(TimeEDA[1])
        elif i < np.shape(TimeDebut)[0] and TimeEDA[0] >= TimeFin[i]:
            #print("i prend plus 1")

            #print(MatriceDebutFin[i][0]+DecallageExclusion, MatriceDebutFin[i][1]-(DecallageExclusion-1))
            #exit()
            




            if len(ListeTempo) > 0:
                                        
                # Resample and process the data
                resampledValues = nk.signal_resample(ListeTempo, sampling_rate=4, desired_sampling_rate=samplingRate, method="interpolation")
                signals, info = nk.eda_process(resampledValues, sampling_rate = samplingRate)

                # On calcule les caracteristiques
                meanPhasic = np.mean(signals["EDA_Phasic"])
                medianPhasic = np.median(signals["EDA_Phasic"])
                stdPhasic = np.std(signals["EDA_Phasic"])
                meanTonic = np.mean(signals["EDA_Tonic"])
                medianTonic = np.median(signals["EDA_Tonic"])
                stdTonic = np.std(signals["EDA_Tonic"])
                npeaks = 0
                for peak in signals["SCR_Peaks"]:
                    npeaks += peak
                auc = integrate.trapz(sorted(signals["EDA_Phasic"]), dx=1)
                maxAmplitudes = max(signals["SCR_Amplitude"])
                sumAmplitudes = np.nansum(signals["SCR_Amplitude"])
                meanAmplitudes = np.nanmean(signals["SCR_Amplitude"])
                kurtosis = stats.kurtosis(signals["EDA_Phasic"])
                skewness = stats.skew(signals["EDA_Phasic"])
                zp99 = np.percentile(signals["EDA_Phasic"], 99)
                skewnessXzp99 = skewness * zp99      
                sumAmplitudeXNpeaks = sumAmplitudes * npeaks 


                data["Numero"].append(NumSeq[i])
                data["ComplexitePercu"].append(Complex[i])
                data["ComplexiteLitterature"].append(ListeComplexiteTheorique[NumSeq[i]-1])

                data["MeanPhasic"].append(meanPhasic)
                data["MedianPhasic"].append(medianPhasic)
                data["STDPhasic"].append(stdPhasic)
                data["MeanTonic"].append(meanTonic)
                data["MedianTonic"].append(medianTonic)
                data["STDTonic"].append(stdTonic)
                data["NPeaks"].append(npeaks)
                data["AUC"].append(auc)
                data["MaxAmplitudes"].append(maxAmplitudes)
                data["SumAmplitudes"].append(sumAmplitudes)
                data["MeanAmplitudes"].append(meanAmplitudes)
                data["Kurtosis"].append(kurtosis)
                data["Skewness"].append(skewness)
                data["Zp99"].append(zp99)
                data["SkewnessXzp99"].append(skewnessXzp99)
                data["SumAmplitudesXNPeaks"].append(sumAmplitudeXNpeaks)

            ListeTempo = []
            i=i+1

    # Fin EDA

    return data


# Fonction modifiée pour traiter un fichier spécifique
def traiter_fichier_musicien_non_musicien(CheminParticipant, CheminDonneesEDA, PerceptionReproduciton, data_musicien, data_non_musicien):
    identifiant_participant = os.path.basename(os.path.dirname(CheminParticipant))
    type_participant = EstMusicien(identifiant_participant)  # 1 pour Musicien, 2 pour Non-Musicien
    
    if type_participant is None:
        print(f"Identifiant non trouvé : {identifiant_participant}")
        return data_musicien, data_non_musicien

    # Appel de la fonction existante pour traiter les fichiers
    data = {
        "Numero": [],
        "ComplexitePercu": [],
        "ComplexiteLitterature": [],
        "Effort": [],
        "MeanPhasic": [],
        "MedianPhasic": [],
        "STDPhasic": [],
        "MeanTonic": [],
        "MedianTonic": [],
        "STDTonic": [],
        "NPeaks": [],
        "AUC": [],
        "MaxAmplitudes": [],
        "SumAmplitudes": [],
        "MeanAmplitudes": [],
        "Kurtosis": [],
        "Skewness": [],
        "Zp99": [],
        "SkewnessXzp99": [],
        "SumAmplitudesXNPeaks": []
    }
    
    # Traitement du fichier EDA et ajout des données dans "data"
    data = traiter_fichier(CheminParticipant, CheminDonneesEDA, PerceptionReproduciton, data)

    # Séparation des données selon qu'il s'agit d'un musicien ou non
    if type_participant == 1:
        for key in data.keys():
            data_musicien[key].extend(data[key])
    elif type_participant == 2:
        for key in data.keys():
            data_non_musicien[key].extend(data[key])
    
    return data_musicien, data_non_musicien



def calculer_moyennes(data):

    # Initialisation des dictionnaires pour chaque niveau de complexité perçue
    data_Sequence = {i: {key: [] for key in data.keys()} for i in range(1, 27)}

    # Parcours des données et séparation selon la complexité perçue
    num_elements = len(data["Numero"])

    print(num_elements)

    for i in range(num_elements):
        Sequence = data["Numero"][i]
        
        # Ajout des données dans le dictionnaire correspondant si l'index existe
        for key in data.keys():
            if i < len(data[key]):
                if 1 <= Sequence <= 27:
                    data_Sequence[Sequence][key].append(data[key][i])

    # Calcul des moyennes pour chaque complexité
    moyennes_complexite = {i: {} for i in range(1, 27)}

    for Sequence, valeurs in data_Sequence.items():
        for key, liste_valeurs in valeurs.items():
            if len(liste_valeurs) > 0:
                moyennes_complexite[Sequence][key] = np.mean(liste_valeurs)
            else:
                moyennes_complexite[Sequence][key] = np.nan  # ou 0 ou None selon vos besoins

    return moyennes_complexite



# Fonction principale modifiée pour gérer musiciens et non-musiciens
def main(dossier_path_Precision, dossier_path_EDA, PerceptionReproduciton):
    # Dictionnaires séparés pour musiciens et non musiciens
    data_musicien = {key: [] for key in ["Numero", "ComplexitePercu", "ComplexiteLitterature", "Effort", "MeanPhasic", "MedianPhasic", "STDPhasic", "MeanTonic", "MedianTonic", "STDTonic", "NPeaks", "AUC", "MaxAmplitudes", "SumAmplitudes", "MeanAmplitudes", "Kurtosis", "Skewness", "Zp99", "SkewnessXzp99", "SumAmplitudesXNPeaks"]}
    data_non_musicien = {key: [] for key in ["Numero", "ComplexitePercu", "ComplexiteLitterature", "Effort", "MeanPhasic", "MedianPhasic", "STDPhasic", "MeanTonic", "MedianTonic", "STDTonic", "NPeaks", "AUC", "MaxAmplitudes", "SumAmplitudes", "MeanAmplitudes", "Kurtosis", "Skewness", "Zp99", "SkewnessXzp99", "SumAmplitudesXNPeaks"]}

    for fichier in os.listdir(dossier_path_Precision):
        chemin_participant = os.path.join(dossier_path_Precision, fichier, "InformationExperience.csv")
        chemin_EDA = os.path.join(dossier_path_EDA, fichier, "EDA.csv")
        data_musicien, data_non_musicien = traiter_fichier_musicien_non_musicien(chemin_participant, chemin_EDA, PerceptionReproduciton, data_musicien, data_non_musicien)
    
    # Calcul des moyennes pour les musiciens et les non musiciens
    moyennes_musicien = calculer_moyennes(data_musicien)
    moyennes_non_musicien = calculer_moyennes(data_non_musicien)

    # Écriture dans les fichiers CSV
    ecrire_moyennes_csv("Moyennes_Musicien.csv", moyennes_musicien)
    ecrire_moyennes_csv("Moyennes_NonMusicien.csv", moyennes_non_musicien)


# Fonction d'écriture des moyennes dans un fichier CSV
def ecrire_moyennes_csv(nom_fichier, moyennes):
    with open(nom_fichier, 'w', newline='') as fichier_csv:
        writer = csv.writer(fichier_csv)
        # En-têtes
        headers = ["Numero"] + list(moyennes[1].keys())
        writer.writerow(headers)
        
        # Écriture des données pour chaque séquence
        for sequence, valeurs in moyennes.items():
            ligne = [sequence] + [valeurs[key] for key in headers[1:]]
            writer.writerow(ligne)


# Appel principal
#dossier_path_Precision = '../Perception/'
dossier_path_Precision = '../Reproduction/'
dossier_path_EDA = '../EDA/'
PerceptionReproduciton = int(sys.argv[1])

main(dossier_path_Precision, dossier_path_EDA, PerceptionReproduciton)
