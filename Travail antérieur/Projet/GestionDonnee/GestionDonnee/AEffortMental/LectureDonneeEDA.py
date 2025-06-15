import sys 
import csv
import numpy as np

import neurokit2 as nk
import statsmodels.api as sm
from scipy import stats, integrate

import CorrelationSpearman


#python3 LecteurDataEDA.py xPerception/Florence/Povel/AAAFinalPerceptionFlorence-Povel2.csv xPerception/Florence/Povel/EDAFlorencePovel.csv 1
#python3 LecteurDataEDA.py xReproduction/Florence/Povel/TestReproductionFinalReprodutionFlorence-Povel2.csv xReproduction/Florence/Povel/EDAFlorencePovel.csv 2


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


# Debut code

# python3 LectureDonneeEDA.py 
#   Perception 
#   EDA 
#   1

if len(sys.argv) == 4:
    CheminParticipant = sys.argv[1]
    CheminDonneesEDA = sys.argv[2]
    PerceptionReproduciton = int(sys.argv[3])
    DecallageExclusion = 2


    #Recupere complexite
    TimeDebut, TimeFin, NumSeq, Complex, Tempo = RecuperationMatrice(CheminParticipant, PerceptionReproduciton)

    ListeComplexiteTheorique = [3.1,3.2,3.1,2.6,2.8,2.5,2.4,3.2,2.4,2.12,2.08,1.80,2.44,3.00,2.04,2.60,3.08,2.56,2.56,2.84,3.60,3.28,3.52,3.60,2.88,4,4]

    """

    for i in NumSeq:
        print(i)
        print(ListeComplexiteTheorique[i-1])
    """

    # Debut Analyse EDA

    samplingRate = 8

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

    #print(np.shape(TimeDebut))

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


    # Debut correlation
    CorrelationSpearmanMeanPhasic = CorrelationSpearman.CalculSpearman(data["ComplexiteLitterature"],data["MeanPhasic"])
    CorrelationSpearmanMedianPhasic = CorrelationSpearman.CalculSpearman(data["ComplexiteLitterature"],data["MedianPhasic"])
    CorrelationSpearmanSTDPhasic = CorrelationSpearman.CalculSpearman(data["ComplexiteLitterature"],data["STDPhasic"])
    CorrelationSpearmanMeanTonic = CorrelationSpearman.CalculSpearman(data["ComplexiteLitterature"],data["MeanTonic"])
    CorrelationSpearmanMedianTonic = CorrelationSpearman.CalculSpearman(data["ComplexiteLitterature"],data["MedianTonic"])
    CorrelationSpearmanSTDTonic = CorrelationSpearman.CalculSpearman(data["ComplexiteLitterature"],data["STDTonic"])

    CorrelationSpearmanNPeaks = CorrelationSpearman.CalculSpearman(data["ComplexiteLitterature"],data["NPeaks"])
    CorrelationSpearmanAUC = CorrelationSpearman.CalculSpearman(data["ComplexiteLitterature"],data["AUC"])
    CorrelationSpearmanMaxAmplitudes = CorrelationSpearman.CalculSpearman(data["ComplexiteLitterature"],data["MaxAmplitudes"])
    CorrelationSpearmanSumAmplitudes = CorrelationSpearman.CalculSpearman(data["ComplexiteLitterature"],data["SumAmplitudes"])
    CorrelationSpearmanMeanAmplitudes = CorrelationSpearman.CalculSpearman(data["ComplexiteLitterature"],data["MeanAmplitudes"])

    CorrelationSpearmanKurtosis = CorrelationSpearman.CalculSpearman(data["ComplexiteLitterature"],data["Kurtosis"])
    CorrelationSpearmanSkewness = CorrelationSpearman.CalculSpearman(data["ComplexiteLitterature"],data["Skewness"])
    CorrelationSpearmanZp99 = CorrelationSpearman.CalculSpearman(data["ComplexiteLitterature"],data["Zp99"])
    CorrelationSpearmanSkewnessXzp99 = CorrelationSpearman.CalculSpearman(data["ComplexiteLitterature"],data["SkewnessXzp99"])



# python3 LectureDonneeEDA.py Perception EDA 1
# python3 LectureDonneeEDA.py Reproduction EDA 2

# python3 LectureDonneeEDA.py ../Perception/1ac9779606a997fda814c4efdbf784679c324f80a0b6168dd4ed089b6a951ef2/InformationExperience.csv ../EDA/1ac9779606a997fda814c4efdbf784679c324f80a0b6168dd4ed089b6a951ef2/EDA.csv 1

