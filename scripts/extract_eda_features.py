#!/usr/bin/env python3
"""Extract basic EDA features from JSON files.

This helper processes all ``*.json`` files inside the given directory and
writes a CSV summary with phasic EDA statistics for each file. It is a
standalone version of the feature extraction used in ``match_eda.py``.
"""

import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd
import neurokit2 as nk
from scipy import integrate
from scipy.stats import kurtosis, skew


def load_eda_json(path: Path) -> tuple[list[float], float]:
    """Return EDA values and sampling rate from an Embrace JSON file."""
    with path.open(encoding="utf-8") as f:
        data = json.load(f)

    # some exports wrap the payload in a single-item list
    if isinstance(data, list):
        data = data[0]

    if "rawData" in data and "eda" in data["rawData"]:
        eda = data["rawData"]["eda"]
    elif "eda" in data:
        eda = data["eda"]
    else:
        raise KeyError("Cannot find EDA data in JSON")

    values = [v for v in eda.get("values", []) if isinstance(v, (int, float))]
    if not values:
        raise ValueError("no EDA values")
    sampling_rate = eda.get("samplingFrequency", 0)
    return values, float(sampling_rate)


def compute_features(values: list[float], sampling_rate: float) -> dict:
    """Return phasic EDA features for a signal."""
    resampled = nk.signal_resample(values, sampling_rate=sampling_rate, desired_sampling_rate=8)
    signals, _ = nk.eda_process(resampled, sampling_rate=8)
    phasic = signals["EDA_Phasic"]
    scr_amp = signals["SCR_Amplitude"]

    return {
        "EDA Phasic Mean": float(np.mean(phasic)),
        "EDA Phasic Median": float(np.median(phasic)),
        "EDA Phasic STD": float(np.std(phasic)),
        "EDA Phasic Number of Peaks": int(np.nansum(signals["SCR_Peaks"])),
        "EDA Phasic AUC": float(integrate.trapz(phasic)),
        "EDA Phasic Max Amplitudes": float(np.nanmax(scr_amp)),
        "EDA Phasic Sum Amplitudes": float(np.nansum(scr_amp)),
        "EDA Phasic Mean Amplitudes": float(np.nanmean(scr_amp)),
        "EDA Phasic Kurtosis": float(kurtosis(phasic)),
        "EDA Phasic Skewness": float(skew(phasic)),
    }


def process_directory(directory: Path) -> pd.DataFrame:
    rows = []
    for json_file in sorted(directory.glob("*.json")):
        try:
            values, sr = load_eda_json(json_file)
        except Exception as e:
            print(f"Skipping {json_file.name}: {e}")
            continue
        if len(values) < 10:
            print(f"Skipping {json_file.name}: too few values")
            continue
        feats = compute_features(values, sr)
        feats["filename"] = json_file.name
        rows.append(feats)
        print(f"Processed {json_file.name}")
    return pd.DataFrame(rows)


def main() -> None:
    parser = argparse.ArgumentParser(description="Compute EDA features for each JSON file")
    parser.add_argument("eda_dir", type=Path, help="Directory containing JSON files")
    parser.add_argument("output_csv", type=Path, nargs="?", default=Path("generated_data/eda_features.csv"), help="Where to save the CSV summary")
    args = parser.parse_args()

    df = process_directory(args.eda_dir)
    args.output_csv.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(args.output_csv, index=False)
    print(f"Wrote {len(df)} rows to {args.output_csv}")


if __name__ == "__main__":
    main()
