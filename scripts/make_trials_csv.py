#!/usr/bin/env python3
# make_trials_csv.py
"""
Créer le fichier time_all_trials.csv au format :
id_participant,task_type,sequence_number,time_beginning,time_ending
À partir du CSV d’origine (participants_with_times.csv).

Usage :
    python make_trials_csv.py participants_with_times.csv  time_all_trials.csv
"""

from __future__ import annotations
import argparse
import csv
from pathlib import Path

# ---------------------------------------------------------------------------

NEEDED = {
    "id_participant",     # hash type a67…
    "task_type",          # Perception / Reproduction
    "numero_sequence",    # 1, 2, 3…
    "time_beginning",     # timestamp (float s)
}

def guess_time_ending(row: dict[str, str]) -> float:
    """Si time_ending absent : duration en secondes × ajouter aux débuts."""
    # → adapté à ton protocole : ici on fixe 30 s par séquence.
    #   Change la logique si tu disposes d’une vraie durée (midi_file etc.).
    BEGIN = float(row["time_beginning"])
    SEQ_DURATION = 30.0          # ← à adapter si besoin
    return BEGIN + SEQ_DURATION

# ---------------------------------------------------------------------------

def main() -> None:
    p = argparse.ArgumentParser(description="Génère time_all_trials.csv")
    p.add_argument("src", type=Path, help="participants_with_times.csv")
    p.add_argument("dst", type=Path, help="time_all_trials.csv à créer")
    args = p.parse_args()

    rows_out: list[dict] = []

    with args.src.open(encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f, delimiter=";")     # ton fichier est séparé par « ; »
        # Vérification du minimum
        missing = NEEDED - set(reader.fieldnames or ())
        if missing:
            raise ValueError(f"Colonnes manquantes : {', '.join(missing)}")

        for r in reader:
            row = {
                "id_participant":  r["id_participant"],
                "task_type":       r["task_type"],
                "sequence_number": r["numero_sequence"],
                "time_beginning":  r["time_beginning"],
                "time_ending":     r.get("time_ending") or guess_time_ending(r),
            }
            rows_out.append(row)

    # Écriture du fichier de sortie (séparateur « , » standard)
    args.dst.parent.mkdir(parents=True, exist_ok=True)
    with args.dst.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "id_participant",
                "task_type",
                "sequence_number",
                "time_beginning",
                "time_ending",
            ],
        )
        writer.writeheader()
        writer.writerows(rows_out)

    print(f"✔ Écrit {len(rows_out)} lignes dans {args.dst}")

if __name__ == "__main__":
    main()
