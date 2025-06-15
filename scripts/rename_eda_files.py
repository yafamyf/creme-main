#!/usr/bin/env python3
"""Rename EDA JSON files according to a mapping.

This helper scans a directory of Embrace JSON exports, reads the
``participantID`` field from each file and renames (or copies) the
file so that its name matches the ``id_participant`` used in
``detections.csv``.

The mapping CSV must contain at least two columns:
``participantID`` (the watch identifier found in the JSON files) and
``id_participant`` (the hashed identifier used in detections.csv).

Example:
    python3 scripts/rename_eda_files.py json/ mapping.csv --output renamed_json/
"""

from __future__ import annotations

import argparse
import csv
import json
import shutil
from pathlib import Path


def load_mapping(path: Path) -> dict[str, str]:
    """Return a dictionary {participantID -> id_participant}."""
    with path.open(newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        if "participantID" not in reader.fieldnames or "id_participant" not in reader.fieldnames:
            raise ValueError("mapping CSV must contain 'participantID' and 'id_participant' columns")
        return {row["participantID"]: row["id_participant"] for row in reader}


def get_participant_id(json_path: Path) -> str | None:
    """Extract participantID from a JSON file."""
    with json_path.open(encoding="utf-8") as f:
        data = json.load(f)
    if isinstance(data, list):
        data = data[0]
    return data.get("participantID") or data.get("rawData", {}).get("participantID")


def process(json_dir: Path, mapping: dict[str, str], out_dir: Path, copy: bool) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    for json_file in json_dir.glob("*.json"):
        pid = get_participant_id(json_file)
        if pid is None:
            print(f"Skipping {json_file.name}: missing participantID")
            continue
        target = mapping.get(pid)
        if not target:
            print(f"No mapping for participantID {pid}, leaving name unchanged")
            target_name = json_file.name
        else:
            target_name = f"{target}.json"
        dest = out_dir / target_name
        if copy:
            shutil.copy2(json_file, dest)
        else:
            json_file.rename(dest)
        print(f"-> {dest}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Rename EDA JSON files using a mapping CSV")
    parser.add_argument("json_dir", type=Path, help="Directory containing original JSON files")
    parser.add_argument("mapping_csv", type=Path, help="CSV mapping participantID to id_participant")
    parser.add_argument("--output", type=Path, default=None, help="Directory to place renamed files (defaults to in-place)")
    parser.add_argument("--copy", action="store_true", help="Copy instead of renaming")
    args = parser.parse_args()

    out_dir = args.output if args.output is not None else args.json_dir
    mapping = load_mapping(args.mapping_csv)
    process(args.json_dir, mapping, out_dir, args.copy)


if __name__ == "__main__":
    main()
