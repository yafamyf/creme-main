import os
import glob
import sys
import csv
import numpy as np
import neurokit2 as nk
import statsmodels.api as sm
from scipy import stats, integrate


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



def calculer_moyennes(data):
    # Initialisation des dictionnaires pour chaque niveau de complexité perçue
    data_complexite = {i: {key: [] for key in data.keys()} for i in range(1, 6)}

    # Parcours des données et séparation selon la complexité perçue
    num_elements = len(data["ComplexitePercu"])

    for i in range(num_elements):
        complexite = data["ComplexitePercu"][i]
        
        # Ajout des données dans le dictionnaire correspondant si l'index existe
        for key in data.keys():
            if i < len(data[key]):
                data_complexite[complexite][key].append(data[key][i])

    # Calcul des moyennes pour chaque complexité
    moyennes_complexite = {i: {} for i in range(1, 6)}

    for complexite, valeurs in data_complexite.items():
        for key, liste_valeurs in valeurs.items():
            if len(liste_valeurs) > 0:
                moyennes_complexite[complexite][key] = np.mean(liste_valeurs)
            else:
                moyennes_complexite[complexite][key] = np.nan  # ou 0 ou None selon vos besoins

    return moyennes_complexite

# Fonction principale pour parcourir les fichiers et calculer les moyennes
def main(dossier_path_Precision, dossier_path_EDA, PerceptionReproduciton):
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


    for fichier in os.listdir(dossier_path_Precision):
        #with open(dossier_path_Precision + fichier + "/" + "InformationExperience.csv", 'r') as file:
        RecuperationMatrice(dossier_path_Precision + fichier + "/" + "InformationExperience.csv", PerceptionReproduciton)
        traiter_fichier(dossier_path_Precision + fichier + "/" + "InformationExperience.csv", dossier_path_EDA + fichier + "/" + "EDA.csv", PerceptionReproduciton, data)


    # Calculer les moyennes après avoir traité tous les fichiers
    moyennes = calculer_moyennes(data)

    for complexite in range(1, 6):
        print(f"Complexité {complexite}:")
        for key, moyenne in moyennes[complexite].items():
            #print(f"{key}: {moyenne}")
            print(f"{moyenne}")
        print("\n")


#Debut du programme // Appel de la fonction principale avec les dossiers

dossier_path_Precision = '../Perception/'
dossier_path_EDA = '../EDA/'
PerceptionReproduciton = int(sys.argv[1])

main(dossier_path_Precision, dossier_path_EDA, PerceptionReproduciton)
