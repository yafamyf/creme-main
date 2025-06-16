#!/usr/bin/env python3
"""Génère un PNG par séquence EDA pour chaque participant.

Usage :
    python build_png_plts.py time_all_trials.csv eda_samples.csv plots_dir

Le fichier ``eda_samples.csv`` doit contenir la colonne ``task_type``.
Si ce n'est pas le cas, celle‑ci est récupérée depuis ``time_all_trials.csv``.
"""
from __future__ import annotations
import argparse
import sys
from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt

# ---------------------------------------------------------------------------
def load_trials(path: Path) -> pd.DataFrame:
    """time_all_trials.csv  →  DataFrame indexé sur (id, sequence)."""
    df = pd.read_csv(path)
    cols = {"id_participant", "task_type", "numero_sequence"}
    if not cols.issubset(df.columns):
        missing = cols - set(df.columns)
        sys.exit(f"✖ colonnes manquantes dans {path.name} : {missing}")
    return df[["id_participant", "task_type", "numero_sequence"]]

def load_samples(path: Path) -> pd.DataFrame:
    """Charge ``eda_samples.csv`` en vérifiant ses colonnes."""
    df = pd.read_csv(path)
    base_cols = {"id_participant", "sequence_number", "timestamp", "eda_value"}
    if not base_cols.issubset(df.columns):
        missing = base_cols - set(df.columns)
        sys.exit(f"✖ colonnes manquantes dans {path.name} : {missing}")
    return df

def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("trials_csv", type=Path)
    p.add_argument("samples_csv", type=Path)
    p.add_argument("out_dir", type=Path)
    args = p.parse_args()

    trials = load_trials(args.trials_csv)
    samples = load_samples(args.samples_csv)

    if "task_type" not in samples.columns:
        # Ajout du type de tâche à partir de time_all_trials.csv
        merged = samples.merge(
            trials,
            left_on=["id_participant", "sequence_number"],
            right_on=["id_participant", "numero_sequence"],
            how="left",
        )
        if merged["task_type"].isna().any():
            nb = merged["task_type"].isna().sum()
            print(f"⚠ {nb} lignes EDA sans séquence correspondante – ignorées.")
            merged = merged.dropna(subset=["task_type"])
    else:
        merged = samples

    # Boucle sur chaque séquence
    for (pid, seq, task), grp in merged.groupby(
        ["id_participant", "sequence_number", "task_type"]
    ):
        out_png = (
            args.out_dir
            / pid
            / task.lower()          # perception / reproduction
            / f"{int(seq)}.png"
        )
        out_png.parent.mkdir(parents=True, exist_ok=True)

        plt.figure(figsize=(10, 3))
        plt.plot(grp["timestamp"] - grp["timestamp"].iloc[0], grp["eda_value"])
        plt.title(f"{pid} – {task} – séquence {int(seq)}")
        plt.xlabel("Temps depuis le début (s)")
        plt.ylabel("EDA (µS)")
        plt.tight_layout()
        plt.savefig(out_png, dpi=150)
        plt.close()

        print(f"✓ {out_png.relative_to(args.out_dir)}")

if __name__ == "__main__":
    main()
