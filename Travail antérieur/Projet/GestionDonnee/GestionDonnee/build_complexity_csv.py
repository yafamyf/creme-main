#!/usr/bin/env python3
import argparse
from pathlib import Path
import pandas as pd

def parse_info_file(path: Path) -> pd.DataFrame:
    # on strippe TOUS les noms de colonnes pour virer les espaces superflus
    df = pd.read_csv(path, skipinitialspace=True)
    df.columns = df.columns.str.strip()
    # on renomme pour usage interne
    df = df.rename(columns={
        "NumeroSequence": "sequence_number",
        "Complexite":       "complexity"
    })
    # on garde seulement ce qui nous intéresse
    return df[["sequence_number", "complexity"]]

def collect_notes(root_dir: Path) -> pd.DataFrame:
    rows = []
    for task in ("Perception", "Reproduction"):
        task_dir = root_dir / task
        if not task_dir.exists():
            continue
        for participant_dir in sorted(task_dir.iterdir()):
            info_file = participant_dir / "InformationExperience.csv"
            if not info_file.exists():
                continue
            try:
                df = parse_info_file(info_file)
            except Exception:
                # en cas de format inattendu, on saute
                continue
            df.insert(0, "id_participant", participant_dir.name)
            df.insert(1, "task_type",       task)
            rows.append(df)
    if not rows:
        return pd.DataFrame(columns=[
            "id_participant","task_type","sequence_number","complexity"
        ])
    return pd.concat(rows, ignore_index=True)

def main():
    p = argparse.ArgumentParser(
        description="Regroupe les notes de complexité par participant et séquence"
    )
    p.add_argument(
        "data_root",
        type=Path,
        nargs="?",
        default=Path("."),
        help="Répertoire contenant Perception/ et Reproduction/"
    )
    p.add_argument(
        "out_csv",
        type=Path,
        help="Chemin du CSV de sortie (e.g. complexity_notes.csv)"
    )
    args = p.parse_args()

    df = collect_notes(args.data_root)
    df.to_csv(args.out_csv, index=False, encoding="utf-8")
    print(f"✅ {len(df)} lignes écrites dans {args.out_csv}")

if __name__ == "__main__":
    main()
