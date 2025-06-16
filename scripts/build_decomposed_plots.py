#!/usr/bin/env python3
"""
Génère un PNG par séquence EDA avec décomposition tonic/phasic.

Usage :
    python build_decomposed_plots.py eda_samples.csv output_dir

Structure d’entrée :
- eda_samples.csv : contient toutes les séquences concaténées
  (avec colonnes : id_participant, task_type, sequence_number, eda_value, timestamp)

Structure de sortie :
- output_dir/
    └── [id_participant]/
        └── [perception|reproduction]/
            └── [n].png (courbes raw/tonic/phasique)
"""

import argparse
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import neurokit2 as nk
import numpy as np

# --------------------------------------------------------------------
def process_and_plot_signal(signal, sampling_rate, save_path, title, output_dir):
    # Neurokit attend au moins quelques dizaines d'échantillons
    if len(signal) < 10:
        print(f"⚠ Trop peu de données ({len(signal)}), ignoré : {save_path}")
        return

    try:
        eda = nk.eda_process(signal, sampling_rate=sampling_rate)
    except Exception as e:
        print(f"✖ Erreur traitement EDA : {e}")
        return

    #df = eda["df"]
    df, _ = nk.eda_process(signal, sampling_rate=sampling_rate)

    t = np.linspace(0, len(df) / sampling_rate, len(df))


    plt.figure(figsize=(10, 3))
    plt.plot(t, df["EDA_Raw"], label="Raw", linewidth=1)
    plt.plot(t, df["EDA_Tonic"], label="Tonic", linewidth=1)
    plt.plot(t, df["EDA_Phasic"], label="Phasic", linewidth=1)
    plt.xlabel("Temps (s)")
    plt.ylabel("EDA (µS)")
    plt.title(title)
    plt.legend()
    plt.tight_layout()
    plt.ylim(0, 12)
    plt.savefig(save_path, dpi=150)
    plt.close()

    print(f"✓ {save_path.relative_to(output_dir)}")




# --------------------------------------------------------------------
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("samples_csv", type=Path, help="eda_samples.csv")
    parser.add_argument("output_dir", type=Path, help="Répertoire de sortie des PNG")
    parser.add_argument("--sampling-rate", type=float, default=4.0, help="Taux d'échantillonnage (Hz)")
    args = parser.parse_args()

    df = pd.read_csv(args.samples_csv)
    required_cols = {"id_participant", "sequence_number", "task_type", "eda_value"}
    if not required_cols.issubset(df.columns):
        missing = required_cols - set(df.columns)
        raise ValueError(f"Colonnes manquantes dans {args.samples_csv}: {missing}")

    for (pid, seq, task), group in df.groupby(["id_participant", "sequence_number", "task_type"]):
        eda_signal = group["eda_value"].values
        title = f"{pid} – {task} – séquence {int(seq)}"
        out_path = args.output_dir / pid / task.lower() / f"{int(seq)}.png"
        out_path.parent.mkdir(parents=True, exist_ok=True)
        process_and_plot_signal(eda_signal, args.sampling_rate, out_path, title, args.output_dir)


if __name__ == "__main__":
    main()
