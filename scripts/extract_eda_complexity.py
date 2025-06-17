#!/usr/bin/env python3
# merge_eda_complexity_with_mapping.py

import argparse
import pandas as pd
from pathlib import Path

def load_mapping(path: Path) -> pd.DataFrame:
    """
    Charge le CSV mapping.csv qui doit contenir au moins deux colonnes :
      - participantID  (ex. "1573-1-1-056")
      - id_participant (le hash, ex. "576019...5391")
    """
    m = pd.read_csv(path, dtype=str)
    # On garde juste les colonnes utiles et on les renomme
    return m[['participantID','id_participant']]

def main():
    parser = argparse.ArgumentParser(
        description="Fusionne EDA + complexité en remplaçant l'id hash par le participantID lisible."
    )
    parser.add_argument("activity_csv",
                        type=Path,
                        help="activity_report.csv (métriques EDA)")
    parser.add_argument("complexity_csv",
                        type=Path,
                        help="complexity_notes.csv (notes de complexité, id_participant = hash)")
    parser.add_argument("mapping_csv",
                        type=Path,
                        help="mapping.csv (participantID ↔ id_participant)")
    parser.add_argument("-o","--out",
                        type=Path,
                        required=True,
                        help="Fichier CSV de sortie")
    args = parser.parse_args()

    # 1) Charger le mapping hash → participantID
    mapping = load_mapping(args.mapping_csv)

    # 2) Charger les métriques EDA
    eda = pd.read_csv(args.activity_csv)
    eda = eda[["id_participant","sequence_number","task_type",
               "max_phasic","nb_scr_peaks","std_raw"]]
    eda["sequence_number"] = eda["sequence_number"].astype(int)
    eda["task_type"]       = eda["task_type"].astype(str)

    # 3) Charger les notes de complexité
    comp = pd.read_csv(args.complexity_csv, dtype={'id_participant':str})
    comp = comp[["id_participant","task_type","sequence_number","complexity"]]
    comp["sequence_number"] = comp["sequence_number"].astype(int)
    comp["task_type"]       = comp["task_type"].astype(str)

    # 4) Fusion EDA + complexité sur (hash, task, seq)
    merged = pd.merge(
        eda,
        comp,
        on=["id_participant","task_type","sequence_number"],
        how="left"
    )

    # 5) Remplacer le hash par le participantID
    merged = merged.merge(
        mapping,
        on="id_participant",
        how="left"
    )
    # si mapping absent, on garde le hash
    merged["participantID"] = merged["participantID"].fillna(merged["id_participant"])

    # 6) Réordonner et renommer
    result = merged[[
        "participantID",
        "sequence_number",
        "task_type",
        "max_phasic",
        "nb_scr_peaks",
        "std_raw",
        "complexity"
    ]].rename(columns={"participantID":"id_participant"})

    # 7) Écrire le CSV
    result.to_csv(args.out, index=False, encoding="utf-8")
    print(f"✅ {len(result)} lignes écrites dans {args.out}")

if __name__ == "__main__":
    main()
