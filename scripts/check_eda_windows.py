#!/usr/bin/env python3
"""Contrôle la cohérence des fenêtres EDA extraites.

Pour chaque séquence présente dans ``time_all_trials.csv`` on calcule :
    - la durée théorique ``time_ending - time_beginning``
    - la durée réelle observée dans ``eda_samples.csv``
    - le nombre d'échantillons enregistrés

Le script affiche les séquences dont les durées ou le nombre
d'échantillons semblent incohérents (écart > 1s ou > 4 échantillons).
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

import pandas as pd


# ---------------------------------------------------------------------------
def load_trials(path: Path) -> pd.DataFrame:
    df = pd.read_csv(path)
    cols = {
        "id_participant",
        "task_type",
        "numero_sequence",
        "time_beginning",
        "time_ending",
    }
    if not cols.issubset(df.columns):
        missing = cols - set(df.columns)
        sys.exit(f"✖ colonnes manquantes dans {path.name} : {missing}")
    return df


def load_samples(path: Path) -> pd.DataFrame:
    df = pd.read_csv(path)
    cols = {"id_participant", "sequence_number", "timestamp", "task_type"}
    if not cols.issubset(df.columns):
        missing = cols - set(df.columns)
        sys.exit(f"✖ colonnes manquantes dans {path.name} : {missing}")
    return df


# ---------------------------------------------------------------------------
def check_windows(trials: pd.DataFrame, samples: pd.DataFrame) -> pd.DataFrame:
    records = []
    for _, t in trials.iterrows():
        mask = (
            (samples["id_participant"] == t["id_participant"])
            & (samples["sequence_number"] == t["numero_sequence"])
            & (samples["task_type"] == t["task_type"])
        )
        grp = samples[mask]
        theo = t["time_ending"] - t["time_beginning"]
        if grp.empty:
            records.append({
                "id": t["id_participant"],
                "seq": t["numero_sequence"],
                "task": t["task_type"],
                "theoretical": theo,
                "real": float("nan"),
                "samples": 0,
                "expected": theo * 4,
            })
            continue
        real = grp["timestamp"].max() - grp["timestamp"].min()
        count = len(grp)
        expected = theo * 4
        records.append({
            "id": t["id_participant"],
            "seq": t["numero_sequence"],
            "task": t["task_type"],
            "theoretical": theo,
            "real": real,
            "samples": count,
            "expected": expected,
        })
    return pd.DataFrame(records)


# ---------------------------------------------------------------------------
def main() -> None:
    parser = argparse.ArgumentParser(description="Diagnostiquer les fenêtres EDA")
    parser.add_argument("trials_csv", nargs="?", default=Path("scripts/time_all_trials.csv"), type=Path)
    parser.add_argument("samples_csv", nargs="?", default=Path("scripts/eda_samples.csv"), type=Path)
    args = parser.parse_args()

    trials = load_trials(args.trials_csv)
    samples = load_samples(args.samples_csv)
    report = check_windows(trials, samples)

    for _, r in report.iterrows():
        theo = r["theoretical"]
        real = r["real"]
        diff = abs(real - theo) if real == real else float("inf")
        count = r["samples"]
        expc = r["expected"]
        diff_c = abs(count - expc)
        msg = (
            f"{r['id']} seq {int(r['seq'])} ({r['task']}): "
            f"theo={theo:.2f}s real={real:.2f}s samples={count} exp≈{expc:.0f}"
        )
        if diff > 1 or diff_c > 4:
            msg += "  -> incohérence"
        print(msg)


if __name__ == "__main__":
    main()
