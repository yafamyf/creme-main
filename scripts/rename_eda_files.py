#!/usr/bin/env python3
"""Rename EDA JSON files according to a mapping.

This helper scans a directory of Embrace JSON exports, reads the
``participantID`` field from each file and renames (or copies) the file
so that its name matches the ``id_participant`` used in ``detections.csv``.

The mapping CSV may :
  • contenir les en-têtes explicites ``participantID,id_participant`` ;
  • être sans en-tête (export Embrace) : on prend alors les colonnes 3 et 4.

Example:
    python scripts/rename_eda_files.py json/ mapping.csv --output renamed_json/
"""

from __future__ import annotations

import argparse
import csv
import json
import shutil
from pathlib import Path


def load_mapping(path: Path) -> dict[str, str]:
    """Return a dictionary {participantID -> id_participant}."""
    with path.open(newline='', encoding='utf-8-sig') as f:
        rows = list(csv.reader(f))

    if not rows:
        return {}

    header = [c.strip() for c in rows[0]]
    # Cas 1 : le CSV a des titres de colonnes explicites
    if 'participantID' in header and 'id_participant' in header:
        pid_idx = header.index('participantID')
        id_idx  = header.index('id_participant')
        data_rows = rows[1:]          # on saute l’en-tête
    # Cas 2 : pas d’en-tête, on suppose colonnes 3 et 4
    else:
        pid_idx, id_idx = 2, 3
        data_rows = rows

    mapping: dict[str, str] = {}
    for row in data_rows:
        if len(row) <= max(pid_idx, id_idx):
            continue
        pid = row[pid_idx].strip()
        target = row[id_idx].strip()
        if pid and target:
            mapping[pid] = target
    return mapping


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
