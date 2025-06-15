import numpy as np
import sys
import neurokit2 as nk
import statsmodels.api as sm
from scipy import stats, integrate
import matplotlib.pyplot as plt

import LecteurDataRecoltes
import CorrelationSpearman

"""
python3 LecteurDataEDA.py ExempleTypiqueDonnees.csv ../DataE4/Daniel/EDA.csv 1 1

python3 LecteurDataEDA.py PremiereDonneePourEDA/DataDanielEssens.csv ../DataE4/Daniel/EDA.csv 1 1
python3 LecteurDataEDA.py PremiereDonneePourEDA/DataDanielPovel.csv ../DataE4/Daniel/EDA.csv 2 1
python3 LecteurDataEDA.py PremiereDonneePourEDA/DataDanielRosenfeld.csv ../DataE4/Daniel/EDA.csv 3 1


python3 LecteurDataEDA.py PremiereDonneePourEDA/DataFlorenceEssens.csv ../DataE4/Florence/EDA.csv 1 1
python3 LecteurDataEDA.py PremiereDonneePourEDA/DataFlorencePovel.csv ../DataE4/Florence/EDA.csv 2 1
python3 LecteurDataEDA.py PremiereDonneePourEDA/DataFlorenceRosenfeld.csv ../DataE4/Florence/EDA.csv 3 1


Deuxieme Florence
python3 LecteurDataEDA.py CheckTimeFlorence/Essens/AFlorence-Essen1.csv CheckTimeFlorence/EDA.csv 1 1
python3 LecteurDataEDA.py CheckTimeFlorence/Povel/AFlorence-Povel2.csv CheckTimeFlorence/EDA.csv 2 1
python3 LecteurDataEDA.py CheckTimeFlorence/Rosenfeld/AFlorence-Rosenfeld3.csv CheckTimeFlorence/EDA.csv 3 1

Deuxieme Corentin
python3 LecteurDataEDA.py CheckTimerCorentin/Essens1/ABrasseur-CorentinEssens1.csv CheckTimerCorentin/EDA.csv 1 1
python3 LecteurDataEDA.py CheckTimerCorentin/Povel1/ABrasseur-CorentinPovel2.csv CheckTimerCorentin/EDA.csv 2 1


Reprodcution Corentin
# python3 LecteurDataEDA.py xReproduction/Corentin/Essens/TestReproductionTestReproduction-TestReproduction.csv xReproduction/Corentin/Essens/EDA.csv 1 2
# python3 LecteurDataEDA.py xReproduction/Corentin/Essens2/TestReproductionTestReproduction-Essens.csv xReproduction/Corentin/Essens2/EDA.csv 1 2
# python3 LecteurDataEDA.py xReproduction/Corentin/Povel/TestReproductionTestReproduction-Povel.csv xReproduction/Corentin/Povel/EDA.csv 2 2



Perception / Reproduction Papa
python3 LecteurDataEDA.py xPerception/Papa/AAAPerceptionPapa-Essens.csv xPerception/Papa/EDA.csv 1 1
python3 LecteurDataEDA.py xReproduction/Papa/TestReproductionFinalReprodutionPapa-Essens.csv xReproduction/Papa/EDA.csv 1 2


Perception / Reproduction Florence

python3 LecteurDataEDA.py xPerception/Florence/Essens/AAAPerceptionFlorence-EssensPerception.csv xPerception/Florence/Essens/EDA.csv 2 1
python3 LecteurDataEDA.py xReproduction/Florence/Essens/BBBBReproductionFlorence-EssensReproduction.csv xReproduction/Florence/Essens/EDA.csv 2 2


Dernier Test
python3 LecteurDataEDA.py xPerception/Florence/Povel/AAAFinalPerceptionFlorence-Povel2.csv xPerception/Florence/Povel/EDAFlorencePovel.csv 2 1
python3 LecteurDataEDA.py xReproduction/Florence/Povel/TestReproductionFinalReprodutionFlorence-Povel2.csv xReproduction/Florence/Povel/EDAFlorencePovel.csv 2 2


"""
if len(sys.argv) == 5:
    CheminPulse = sys.argv[1]
    CheminDonnees = sys.argv[2]
    NumeroDatabase = int(sys.argv[3])
    PerceptionReproduciton = int(sys.argv[4])
else:
    CheminPulse = "ExempleTypiqueDonnees.csv"
    CheminDonnees = "../DataE4/Daniel/EDA.csv"
    NumeroDatabase = 1
    PerceptionReproduciton = 1

#DecallageExclusion = 0
DecallageExclusion = 2

MatriceDebutFin = LecteurDataRecoltes.main(CheminPulse, PerceptionReproduciton)


ComplexiteESSENSLitterature = [2.2,3.1,3.2,2.9,2.2,3.1,2.6,4.2,2.9,2.8,3.1,2.5,3.5,2.5,2.4,3.0,3.0,3.1,2.4,3.2,2.4,2.9,2.7,3.8]
###
ComplexiteESSENSFlorence = [2,2,2,2,2,2,2,3,2,2,3,2,3,3,3,4,1,3,2,3,2,5,3,2]
###


ComplexitePOVELLitterature = [1.56,2.12,2.08,1.88,1.80,2.44,2.20,2.56,3.00,2.04,2.76,2.72,3.00,3.16,2.04,2.88,2.60,2.60,2.64,3.24,3.08,3.04,3.04,2.56,2.56,2.84,3.60,2.68,3.28,3.08,3.52,3.60,3.04,2.88,3.08]
###
ComplexitePOVELFlorence = [2,2,2,2,2,2,2,2,3,2,2,2,2,2,2,2,2,2,2,2,2,3,3,3]
###

ComplexiteRosenfeldPercueFlorence = [5,1,3,3,3,4,4,4,5,4,3,3,1,5,3,3,3,3,2,3,5,1,5,5,3,4,5,4,2,2]
ComplexiteRosenfeldPercueCorentin = [1,2,1,1,1,2,4,3,2,4,2,2,3,4,5,2,2,1,1,3,4,1,4,2,1,4,2,3,2,3]

###
ComplexiteESSENSReproductionCorentin = [2,1,4,4,5,4,5,4,5,2,1,1,2,2,3,3,4,2,3,2,2,3,1,4]
###


if NumeroDatabase == 1:
    Database = ComplexiteESSENSLitterature 
elif NumeroDatabase == 2:
    Database = ComplexitePOVELLitterature 
elif NumeroDatabase == 3:
    Database = ComplexiteRosenfeldPercueFlorence
elif NumeroDatabase == 4:
    Database = ComplexiteRosenfeldPercueCorentin
else:
    #Database = ComplexiteESSENSLitterature 
    Database = ComplexiteESSENSReproductionCorentin
#for TimeSequence in MatriceDebutFin:
#    print(TimeSequence[0], TimeSequence[1])


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
with open(CheminDonnees, 'r') as file:
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


""" Deuxieme compartiment
#######################
#######################
#######################
#######################
#######################
"""

i=0
ListeTempo=[]

print(np.shape(MatriceDebutFin))

for TimeEDA in matriceTime:
    #Si je ne suis pas arrivé à la derniere sequence
    if (i < np.shape(MatriceDebutFin)[0] and 
    #Je prend le temps debut de ma sequence + une constante
    TimeEDA[0] >= (MatriceDebutFin[i][0]+DecallageExclusion) and
    #Je vais jusque la fin de la sequence (faut que je la calcule via le tempo) 
    # - constance, (ca a l'air beaucoup, ptet reduire c et modifier en +2*c et -c plus tard)
    TimeEDA[0] <= MatriceDebutFin[i][1]-(DecallageExclusion-1)):

        ListeTempo.append(TimeEDA[1])
    elif i < np.shape(MatriceDebutFin)[0] and TimeEDA[0] >= MatriceDebutFin[i][1]:
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


            data["Numero"].append(MatriceDebutFin[i][2])
            data["ComplexitePercu"].append(MatriceDebutFin[i][3])
            data["ComplexiteLitterature"].append(Database[MatriceDebutFin[i][2]-1])

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

"""
print(data["MeanPhasic"])
print(data["ComplexitePercu"])
print(data["ComplexiteLitterature"])
print(data["NPeaks"])
"""

#tempo = 0

"""
for tempo in range(30,40):
    print(data["Numero"][tempo])
    print(data["MeanPhasic"][tempo])
    print(data["MedianPhasic"][tempo])
    print(data["STDPhasic"][tempo])
    print(data["MeanTonic"][tempo])
    print(data["MedianTonic"][tempo])
    print(data["STDTonic"][tempo])
    print(data["NPeaks"][tempo])
    print(data["AUC"][tempo])
    print(data["MaxAmplitudes"][tempo])
    print(data["SumAmplitudes"][tempo])
    print(data["MeanAmplitudes"][tempo])
    print(data["Kurtosis"][tempo])
    print(data["Skewness"][tempo])
    print(data["Zp99"][tempo])
    print(data["SkewnessXzp99"][tempo])
    print(" ")

"""

"""
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
"""



#with open('Sortie.txt', 'a') as file:
with open('MatriceData.txt', 'w') as file:

    #print("")
    print(data["Numero"], file=file)
    #print("")
    print(data["MeanPhasic"], file=file)
    #print("")
    print(data["MedianPhasic"], file=file)
    #print("")
    print(data["STDPhasic"], file=file)
    #print("")
    print(data["MeanTonic"], file=file)
    #print("")
    print(data["MedianTonic"], file=file)
    #print("")
    print(data["STDTonic"], file=file)
    #print("")
    print(data["NPeaks"], file=file)
    #print("")
    print(data["AUC"], file=file)
    #print("")
    print(data["MaxAmplitudes"], file=file)
    #print("")
    print(data["SumAmplitudes"], file=file)
    #print("")
    print(data["MeanAmplitudes"], file=file)
    #print("")
    print(data["Kurtosis"], file=file)
    #print("")
    print(data["Skewness"], file=file)
    #print("")
    print(data["Zp99"], file=file)
    #print("")
    print(data["SkewnessXzp99"], file=file)
