import pandas as pd

df = pd.read_csv("effort_eda_merged.csv")
print(df.shape)
print(df[['std_raw','max_phasic','area_phasic','nb_scr_peaks','complexity','motivation','fatigue']].head(10))
