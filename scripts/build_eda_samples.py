#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Construit ``eda_samples.csv`` en associant chaque fenêtre EDA
à un participant, un type de tâche et un numéro de séquence.
"""

import argparse
from pathlib import Path
import pandas as pd

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("trials_csv", type=Path, help="time_all_trials.csv")
    parser.add_argument("eda_csv",    type=Path, help="time_all_eda_values.csv")
    parser.add_argument("out_csv",    type=Path, help="fichier de sortie")
    args = parser.parse_args()

    trials = pd.read_csv(args.trials_csv)
    eda    = pd.read_csv(args.eda_csv)

    final_rows = []

    for (pid, task), grp in trials.groupby(["id_participant", "task_type"]):
        for seq, row in grp.groupby("numero_sequence").first().iterrows():
            t0, t1 = row["time_beginning"], row["time_ending"]

            eda_win = eda[(eda["timestamp"] >= t0) & (eda["timestamp"] <= t1)]
            if eda_win.empty:
                continue

            final_rows.append(
                pd.DataFrame({
                    "id_participant": pid,
                    "task_type": task,
                    "sequence_number": seq,
                    "timestamp": eda_win["timestamp"].values,
                    "eda_value": eda_win["eda_value"].values,
                })
            )

    # concaténer et sauvegarder
    result = (
        pd.concat(final_rows, ignore_index=True)
        if final_rows
        else pd.DataFrame(
            columns=["id_participant", "task_type", "sequence_number", "timestamp", "eda_value"]
        )
    )
    result.to_csv(args.out_csv, index=False, encoding="utf-8")
    print(f"✅ {len(result):,} lignes écrites dans {args.out_csv}")

if __name__ == "__main__":
    main()
