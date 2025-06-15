import csv
from pathlib import Path

BASE = Path('Travail antérieur/Projet/GestionDonnee/GestionDonnee')
SEQUENCE_DIR = Path('Travail antérieur/Projet/Sequence/SequenceRythme')
TASKS = ['Perception', 'Reproduction']

rows = []
for task in TASKS:
    task_dir = BASE / task
    if not task_dir.is_dir():
        continue
    for participant in sorted(task_dir.iterdir()):
        if not participant.is_dir():
            continue
        info_csv = participant / 'InformationExperience.csv'
        if not info_csv.exists():
            continue
        with info_csv.open() as f:
            reader = csv.DictReader(f, skipinitialspace=True)
            for r in reader:
                try:
                    t0 = float(r['Time Absolue'])
                    seq = int(r['NumeroSequence'])
                except (KeyError, ValueError):
                    continue
                midi = SEQUENCE_DIR / f'SequenceNumero{seq}.mid'
                rows.append({
                    'id_participant': participant.name,
                    'task_type': task,
                    'numero_sequence': seq,
                    'time_beginning': t0,
                    'midi_file': str(midi)
                })

rows.sort(key=lambda x: (x['id_participant'], x['task_type'], x['time_beginning']))

out_path = Path('detections.csv')
with out_path.open('w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=['id_participant','task_type','numero_sequence','time_beginning','midi_file'])
    writer.writeheader()
    writer.writerows(rows)
print(f'Wrote {len(rows)} rows to {out_path}')

