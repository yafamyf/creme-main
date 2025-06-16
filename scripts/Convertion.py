from pathlib import Path
import json
import argparse
import fastavro

def avro_to_json(avro_path: Path, json_path: Path) -> None:
    """Lit *avro_path* et écrit un tableau JSON de ses enregistrements dans *json_path*."""
    with avro_path.open('rb') as f:
        records = list(fastavro.reader(f))          # → liste de dict
    json_path.parent.mkdir(parents=True, exist_ok=True)
    with json_path.open('w', encoding='utf-8') as f:
        json.dump(records, f, ensure_ascii=False, indent=2)
    print(f"✓ {json_path}")

def batch(src_dir: Path, dst_dir: Path) -> None:
    """Parcourt src_dir à la recherche de *.avro* et les convertit tous."""
    for avro_file in src_dir.rglob('*.avro'):
        out_file = dst_dir / f"{avro_file.stem}.json"
        avro_to_json(avro_file, out_file)

if __name__ == "__main__":
    p = argparse.ArgumentParser(description="Convertir un lot d'AVRO en JSON")
    p.add_argument("src", type=Path, help="Dossier contenant les .avro")
    p.add_argument("dst", type=Path, help="Dossier de sortie pour les .json")
    args = p.parse_args()
    batch(args.src, args.dst)
