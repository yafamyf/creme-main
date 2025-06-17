#!/usr/bin/env python3
# build_effort_mental_csv.py

import argparse
from pathlib import Path
import pandas as pd

def main():
    parser = argparse.ArgumentParser(
        description="Agrège tous les MotivationFatigue.csv en un seul CSV"
    )
    parser.add_argument(
        "gestion_root",
        type=Path,
        help="chemin vers GestionDonnee/GestionDonnee (contenant Perception/, Reproduction/)"
    )
    parser.add_argument(
        "out_csv",
        type=Path,
        help="chemin du CSV de sortie (effort_mental.csv)"
    )
    args = parser.parse_args()

    rows = []
    for task in ("Perception", "Reproduction"):
        task_dir = args.gestion_root / task
        if not task_dir.is_dir():
            continue
        for part in task_dir.iterdir():
            mf = part / "MotivationFatigue.csv"
            if not mf.exists():
                continue
            df = pd.read_csv(mf, names=["block", "motivation", "fatigue"])
            df["id_participant"] = part.name
            rows.append(df[["id_participant", "block", "motivation", "fatigue"]])

    if not rows:
        print("⚠️  Aucun fichier MotivationFatigue.csv trouvé")
        return

    result = pd.concat(rows, ignore_index=True)
    result.to_csv(args.out_csv, index=False, encoding="utf-8")
    print(f"✅ {len(result)} lignes écrites dans {args.out_csv}")

if __name__ == "__main__":
    main()
