"""Enrich trial information with mean EDA values.

This utility reads ``time_all_trials.csv`` and all JSON exports present in the
``avro_json`` directory. For each trial window it computes the mean of the
ElectroDermal Activity (EDA) signal inside that window and writes the result
back to ``time_all_trials.csv`` replacing the previous file.

The JSON files are assumed to follow the structure exported by the Embrace
watch where EDA data is found under ``rawData.eda``. Large numeric
``timestampStart`` values are automatically converted from microseconds to
seconds.

Usage::

    python enrich_trials_with_eda.py [csv_path] [json_dir]

The default paths are ``scripts/time_all_trials.csv`` and
``scripts/avro_json`` respectively.
"""
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path


def load_eda_json(path: Path) -> tuple[float, float, list[float]]:
    """Return ``(start, freq, values)`` from one JSON file."""
    with path.open(encoding="utf-8") as f:
        data = json.load(f)

    if isinstance(data, list):
        data = data[0]

    if "rawData" in data and "eda" in data["rawData"]:
        eda = data["rawData"]["eda"]
    elif "eda" in data:
        eda = data["eda"]
    else:
        raise KeyError(f"Cannot find EDA data in {path.name}")

    start = eda.get("timestampStart", 0)
    if start > 1_000_000_000_000:
        start /= 1_000_000  # microseconds → seconds
    freq = float(eda.get("samplingFrequency", 0)) or 4.0
    values = [float(v) for v in eda.get("values", [])]
    return start, freq, values


def accumulate_for_trials(json_file: Path, trials: list[dict]) -> None:
    """Add EDA values from *json_file* to all overlapping trials."""
    start, freq, values = load_eda_json(json_file)
    if not values:
        return
    end = start + len(values) / freq

    for t in trials:
        if t["time_ending"] < start or t["time_beginning"] > end:
            continue
        i0 = max(0, int((t["time_beginning"] - start) * freq))
        i1 = min(len(values), int((t["time_ending"] - start) * freq) + 1)
        if i0 >= i1:
            continue
        segment = values[i0:i1]
        t["eda_sum"] += sum(segment)
        t["eda_count"] += len(segment)


def main() -> None:
    parser = argparse.ArgumentParser(description="Compute mean EDA for each trial")
    parser.add_argument("csv_path", nargs="?", default=Path("scripts/time_all_trials.csv"), type=Path)
    parser.add_argument("json_dir", nargs="?", default=Path("scripts/avro_json"), type=Path)
    args = parser.parse_args()

    trials: list[dict] = []
    with args.csv_path.open(encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for r in reader:
            trials.append({
                "id_participant": r["id_participant"],
                "task_type": r["task_type"],
                "numero_sequence": r["numero_sequence"],
                "time_beginning": float(r["time_beginning"]),
                "time_ending": float(r["time_ending"]),
                "eda_sum": 0.0,
                "eda_count": 0,
            })

    for json_file in sorted(args.json_dir.glob("*.json")):
        try:
            accumulate_for_trials(json_file, trials)
        except Exception:
            continue

    fieldnames = [
        "id_participant",
        "task_type",
        "numero_sequence",
        "time_beginning",
        "time_ending",
        "eda_mean",
    ]

    with args.csv_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for t in trials:
            mean = t["eda_sum"] / t["eda_count"] if t["eda_count"] else ""
            writer.writerow({
                "id_participant": t["id_participant"],
                "task_type": t["task_type"],
                "numero_sequence": t["numero_sequence"],
                "time_beginning": t["time_beginning"],
                "time_ending": t["time_ending"],
                "eda_mean": mean,
            })


if __name__ == "__main__":
    main()
