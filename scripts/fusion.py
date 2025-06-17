import pandas as pd
import glob, pathlib

# a) EDA
eda = pd.read_csv("activity_report.csv")

# b) complexité (un fichier par participant)
rows = []
for f in glob.glob(r"..\Travail antérieur\Projet\GestionDonnee\*\InformationExperience.csv"):
    tmp = pd.read_csv(f, names=["time_abs","time_rel","sequence_number",
                                "tempo","complexity"])
    tmp["id_participant"] = pathlib.Path(f).parent.name          # le dossier = id
    tmp["task_type"] = "Perception"       # ou Reproduction si besoin
    rows.append(tmp[["id_participant","sequence_number","complexity"]])
complx = pd.concat(rows, ignore_index=True)

# c) fatigue / motivation (même principe)
motfat = []
for f in glob.glob(r"..\Travail antérieur\Projet\GestionDonnee\*\MotivationFatigue.csv"):
    tmp = pd.read_csv(f, names=["block","motiv","fatigue"])
    tmp["id_participant"] = pathlib.Path(f).parent.name
    motfat.append(tmp)
motfat = pd.concat(motfat, ignore_index=True)

# on recolle fatigue/motivation à chaque séquence
complx["block"] = (complx["sequence_number"]-1)//10*5      # 0,10,15,20
df = complx.merge(motfat, on=["id_participant","block"], how="left")

# fusion finale
merged = eda.merge(df, on=["id_participant","sequence_number","task_type"], how="inner")
merged.to_csv("effort_eda_merged.csv", index=False)
