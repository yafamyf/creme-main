#!/usr/bin/env python3
"""Match EDA values with trials using timestamps only."""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt


def load_trials(path: Path) -> pd.DataFrame:
    df = pd.read_csv(path)
    required = {"id_participant", "task_type", "sequence_number", "time_beginning", "time_ending"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"Missing columns in trials CSV: {missing}")
    return df


def load_eda(path: Path) -> pd.DataFrame:
    df = pd.read_csv(path)
    required = {"timestamp", "eda_value"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"Missing columns in EDA CSV: {missing}")
    return df


def match_and_plot(trials: pd.DataFrame, eda: pd.DataFrame, out_dir: Path) -> pd.DataFrame:
    rows = []
    for _, row in trials.iterrows():
        t0, t1 = row["time_beginning"], row["time_ending"]
        window = eda[(eda["timestamp"] >= t0) & (eda["timestamp"] <= t1)]
        for _, r in window.iterrows():
            rows.append({
                "id_participant": row["id_participant"],
                "sequence_number": row["sequence_number"],
                "timestamp": r["timestamp"],
                "eda_value": r["eda_value"],
            })
        if not window.empty:
            out_path = out_dir / str(row["id_participant"]) / row["task_type"] / f"{row['sequence_number']}.png"
            out_path.parent.mkdir(parents=True, exist_ok=True)
            plt.figure(figsize=(10, 4))
            plt.plot(window["timestamp"], window["eda_value"], label="EDA")
            plt.xlabel("timestamp")
            plt.ylabel("EDA")
            plt.tight_layout()
            plt.savefig(out_path)
            plt.close()
    return pd.DataFrame(rows)


def main() -> None:
    parser = argparse.ArgumentParser(description="Match EDA values by timestamp range")
    parser.add_argument("trials_csv", type=Path, help="CSV with time ranges")
    parser.add_argument("eda_csv", type=Path, help="CSV with all EDA values")
    parser.add_argument("out_dir", type=Path, help="Output directory for PNGs")
    parser.add_argument("output_csv", type=Path, help="Path for merged CSV")
    args = parser.parse_args()

    trials = load_trials(args.trials_csv)
    eda = load_eda(args.eda_csv)
    merged = match_and_plot(trials, eda, args.out_dir)
    merged.to_csv(args.output_csv, index=False)


if __name__ == "__main__":
    main()

