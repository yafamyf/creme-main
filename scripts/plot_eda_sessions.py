import csv
from pathlib import Path
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parent.parent
DETECTION_CSV = ROOT / 'detections.csv'
EDA_ROOT = ROOT / 'Travail antérieur' / 'Projet' / 'GestionDonnee' / 'GestionDonnee' / 'EDA'

OUT_DIR = ROOT / 'eda_overview'

# Load detection times
rows = []
with DETECTION_CSV.open(encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for r in reader:
        rows.append({
            'id': r['id_participant'],
            'task': r['task_type'],
            'time': float(r['time_beginning'])
        })

# group by participant and task
from collections import defaultdict

span = defaultdict(lambda: {'start': float('inf'), 'end': 0})
for r in rows:
    key = (r['id'], r['task'])
    if r['time'] < span[key]['start']:
        span[key]['start'] = r['time']
    if r['time'] > span[key]['end']:
        span[key]['end'] = r['time']
# add 10s margin after last detection
for key in span:
    span[key]['end'] += 10

for (pid, task), se in span.items():
    eda_file = EDA_ROOT / pid / 'EDA.csv'
    if not eda_file.exists():
        print(f'Missing EDA for {pid}')
        continue
    with eda_file.open() as f:
        start_ts = float(f.readline().strip())
        freq = float(f.readline().strip())
        values = [float(line.strip()) for line in f if line.strip()]
    times = [start_ts + i / freq for i in range(len(values))]
    # slice window
    t = []
    v = []
    for tt, vv in zip(times, values):
        if se['start'] <= tt <= se['end']:
            t.append(tt - se['start'])
            v.append(vv)
    if not t:
        continue
    out_dir = OUT_DIR / pid
    out_dir.mkdir(parents=True, exist_ok=True)
    plt.figure(figsize=(10, 4))
    plt.plot(t, v, color='blue')
    plt.xlabel('seconds from first detection')
    plt.ylabel('EDA')
    plt.title(f'{pid} - {task}')
    plt.tight_layout()
    plt.savefig(out_dir / f'{task}.png')
    plt.close()
