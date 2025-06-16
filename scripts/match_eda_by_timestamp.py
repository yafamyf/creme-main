# -*- coding: utf-8 -*-
"""Match detection windows with EDA values using timestamps only.

This script builds two intermediate CSV files:
    - ``time_all_trials.csv`` containing all detection windows
    - ``time_all_eda_values.csv`` gathering EDA timestamps from all JSON exports

It then generates a final CSV ``merged_eda_trials.csv`` where each line
corresponds to a timestamped EDA value linked to a participant and
sequence number.

Example usage:

    python3 match_eda_by_timestamp.py detections.csv json_dir generated_data/

The JSON directory is scanned recursively for ``*.json`` files. Each file
must follow the structure exported by Embrace (``rawData.eda`` or legacy
fields at the root).
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Iterable

import pandas as pd


# ---------------------------------------------------------------------------
# Helpers copied and adapted from match_eda.py
# ---------------------------------------------------------------------------

def midi_duration(midi_path: Path) -> float:
    """Return the duration of a MIDI file in seconds."""
    try:
        import mido
    except ImportError as exc:
        raise ImportError("mido library required to compute MIDI duration") from exc

    m = mido.MidiFile(midi_path)
    return m.length


def load_detection_csv(path: Path) -> pd.DataFrame:
    """Load detection CSV and compute time_ending if missing."""
    df = pd.read_csv(path)

    required = {"id_participant", "task_type", "numero_sequence", "time_beginning"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"Missing columns in detection CSV: {missing}")

    if "time_ending" not in df.columns:
        if "midi_file" not in df.columns:
            raise ValueError("CSV must contain either 'time_ending' or 'midi_file' column")

        durations: dict[Path, float] = {}

        def compute_end(row: pd.Series) -> float:
            midi_path = Path(row["midi_file"])
            if midi_path not in durations:
                durations[midi_path] = midi_duration(midi_path)
            return row["time_beginning"] + durations[midi_path]

        df["time_ending"] = df.apply(compute_end, axis=1)

    return df


def load_eda_json(path: Path) -> pd.DataFrame:
    """Load EDA timestamps and values from an Embrace JSON export."""
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    if isinstance(data, list):
        data = data[0]

    if "rawData" in data and "eda" in data["rawData"]:
        eda = data["rawData"]["eda"]
    elif "eda" in data:
        eda = data["eda"]
    else:
        raise KeyError("Cannot find EDA data in JSON")

    start = eda["timestampStart"]
    if start > 1_000_000_000_000:
        start /= 1_000_000

    freq = eda["samplingFrequency"]
    values = eda["values"]
    timestamps = [start + i / freq for i in range(len(values))]
    return pd.DataFrame({"timestamp": timestamps, "eda_value": values})


def load_all_eda_jsons(directory: Path) -> pd.DataFrame:
    """Concatenate EDA values from all JSON files under *directory*."""
    frames: list[pd.DataFrame] = []
    for json_path in directory.rglob("*.json"):
        try:
            df = load_eda_json(json_path)
        except Exception:
            continue
        frames.append(df)
    if not frames:
        return pd.DataFrame(columns=["timestamp", "eda_value"])
    all_df = pd.concat(frames, ignore_index=True)
    all_df.sort_values("timestamp", inplace=True)
    all_df.reset_index(drop=True, inplace=True)
    return all_df


# ---------------------------------------------------------------------------
# Matching by timestamp
# ---------------------------------------------------------------------------

def match_trials_with_eda(trials: pd.DataFrame, eda: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for _, t in trials.iterrows():
        t0 = t["time_beginning"]
        t1 = t["time_ending"]
        window = eda[(eda["timestamp"] >= t0) & (eda["timestamp"] <= t1)]
        if window.empty:
            continue
        for _, r in window.iterrows():
            rows.append({
                "id_participant": t["id_participant"],
                "sequence_number": t["numero_sequence"],
                "timestamp": r["timestamp"],
                "eda_value": r["eda_value"],
            })
    return pd.DataFrame(rows)


# ---------------------------------------------------------------------------
# Main entry
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(description="Merge EDA values with detection times using timestamps")
    parser.add_argument("detection_csv", type=Path, help="CSV with detection data")
    parser.add_argument("eda_dir", type=Path, help="Directory containing EDA JSON files")
    parser.add_argument("output_dir", type=Path, help="Directory to store CSV outputs")
    args = parser.parse_args()

    args.output_dir.mkdir(parents=True, exist_ok=True)

    trials = load_detection_csv(args.detection_csv)[[
        "id_participant",
        "task_type",
        "numero_sequence",
        "time_beginning",
        "time_ending",
    ]]
    trials.to_csv(args.output_dir / "time_all_trials.csv", index=False)

    eda = load_all_eda_jsons(args.eda_dir)
    eda.to_csv(args.output_dir / "time_all_eda_values.csv", index=False)

    merged = match_trials_with_eda(trials, eda)
    merged.to_csv(args.output_dir / "merged_eda_trials.csv", index=False)


if __name__ == "__main__":
    main()
