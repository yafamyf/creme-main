#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Construit eda_samples.csv
(id_participant → task_type → sequence_number)
"""
import argparse
from pathlib import Path
import pandas as pd

def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("trials_csv", type=Path)
    p.add_argument("eda_csv",    type=Path)
    p.add_argument("out_csv",    type=Path)
    args = p.parse_args()

    trials = pd.read_csv(args.trials_csv)
    eda    = pd.read_csv(args.eda_csv)

    rows = []

    for pid in trials["id_participant"].unique():
        for _, t in trials[trials.id_participant == pid].iterrows():
            seq  = t["numero_sequence"]
            t0, t1 = t["time_beginning"], t["time_ending"]

            win = eda[(eda.timestamp >= t0) & (eda.timestamp <= t1)]
            if win.empty:
                continue

            # ----------- filtrage : segment contigu qui démarre à t0 ----------
            win = win.sort_values("timestamp").reset_index(drop=True)
            dt  = win.timestamp.diff().fillna(0)
            cut = dt[dt > 1.0].index          # trou > 1 s  (seuil ajustable)
            if not cut.empty:
                win = win.loc[: cut[0]-1]
            if win.empty:
                continue
            # ------------------------------------------------------------------

            rows.append(pd.DataFrame({
                "id_participant": pid,
                "sequence_number": seq,
                "timestamp":      win.timestamp.values,
                "eda_value":      win.eda_value.values,
            }))

    out = (pd.concat(rows, ignore_index=True)
           if rows else
           pd.DataFrame(columns=["id_participant","sequence_number","timestamp","eda_value"]))
    out.to_csv(args.out_csv, index=False, encoding="utf-8")
    print(f"✅ {len(out):,} lignes écrites dans {args.out_csv}")

if __name__ == "__main__":
    main()
