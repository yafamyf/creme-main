# scripts/check_alignment.py
import pandas as pd, sys, pathlib
trials  = pd.read_csv(pathlib.Path(sys.argv[1]))           # time_all_trials.csv
samples = pd.read_csv(pathlib.Path(sys.argv[2]))           # eda_samples.csv

bad = []
for (_, t) in trials.iterrows():
    seg = samples[(samples.id_participant == t.id_participant) &
                  (samples.sequence_number == t.numero_sequence)]
    if seg.empty: 
        bad.append((t.id_participant, t.numero_sequence, 'AUCUN échantillon'))
        continue
    dt_theo = t.time_ending - t.time_beginning
    dt_real = seg.timestamp.max() - seg.timestamp.min()
    n_exp   = dt_theo * 4
    if abs(dt_real - dt_theo) > 1 or len(seg) < n_exp*0.6:
        bad.append((t.id_participant, t.numero_sequence,
                    f'durée théorique {dt_theo:.1f}s  /  réelle {dt_real:.1f}s  '
                    f'({len(seg)} pts, attendu ≃ {n_exp:.0f})'))
print('\n'.join(map(str,bad)) if bad else 'Tout est cohérent ✅')
