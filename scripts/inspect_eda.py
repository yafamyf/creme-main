import pandas as pd

df = pd.read_csv("eda_samples.csv")

print(df["eda_value"].describe())
