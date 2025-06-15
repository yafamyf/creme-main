#!/usr/bin/env python3
"""Convert multiple EDA JSON files to a single CSV with timestamps."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import pandas as pd


def parse_json(path: Path) -> pd.DataFrame:
    with path.open() as f:
        data = json.load(f)
    if isinstance(data, list):
        data = data[0]
    try:
        eda = data["rawData"]["eda"]
    except (KeyError, TypeError) as e:
        raise ValueError(f"Missing EDA data in {path}") from e

    ts_start = eda["timestampStart"] / 1_000_000
    freq = eda["samplingFrequency"]
    values = eda.get("values") or []
    timestamps = [ts_start + i / freq for i in range(len(values))]
    return pd.DataFrame({"timestamp": timestamps, "eda_value": values})


def main() -> None:
    parser = argparse.ArgumentParser(description="Merge EDA JSON files into a CSV")
    parser.add_argument("json_dir", type=Path, help="Directory containing JSON files")
    parser.add_argument("output_csv", type=Path, help="Path to output CSV")
    args = parser.parse_args()

    rows = []
    for path in sorted(args.json_dir.glob("*.json")):
        try:
            df = parse_json(path)
        except ValueError as e:
            print(e)
            continue
        rows.append(df)
    if rows:
        result = pd.concat(rows).sort_values("timestamp")
    else:
        result = pd.DataFrame(columns=["timestamp", "eda_value"])
    result.to_csv(args.output_csv, index=False)


if __name__ == "__main__":
    main()
