#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Associe chaque séquence expérimentale à sa fenêtre EDA, calcule
dix indicateurs phasiques, puis sauvegarde :

  • merged.csv   – tous les échantillons alignés
  • features.csv – 1 ligne par séquence : 10 métriques
  • plots/<id>/<perception|reproduction>/<n>.png

Usage
------
python match_eda.py detections.csv renamed_json/ plots/ merged.csv features.csv \
       --midi-dir midi/ --resample 4
"""
from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import neurokit2 as nk

# ──────────────────────────────────────────────────────────────
# Options CLI
# ──────────────────────────────────────────────────────────────
def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser("Faire correspondre EDA ↔ séquences")
    p.add_argument("detections_csv", type=Path)
    p.add_argument("eda_dir",        type=Path, help="*.json renommés")
    p.add_argument("plots_dir",      type=Path)
    p.add_argument("merged_csv",     type=Path)
    p.add_argument("features_csv",   type=Path)
    p.add_argument("--midi-dir",     type=Path, default=None,
                   help="Si time_ending absent : dossier des .mid")
    p.add_argument("--resample",     type=float, default=4.0,
                   help="Fréquence cible (Hz) – 4 Hz par défaut")
    return p.parse_args()

# ──────────────────────────────────────────────────────────────
# Outils
# ──────────────────────────────────────────────────────────────
def load_json(path: Path) -> pd.DataFrame:
    """Lit un export Empatica déjà renommé et renvoie un DataFrame."""
    with path.open(encoding="utf-8") as f:
        data = json.load(f)
    meta, records = data["info"], data["signal"]["values"]
    sfreq      = float(meta["samplingFrequency"])
    t0_us      = int(meta["timestampStart"])
    timestamps = (t0_us + np.arange(len(records))*1e6/sfreq) / 1e6  # → s
    return pd.DataFrame({"timestamp": timestamps, "eda_value": records})

def midi_duration(mid_path: Path) -> float:
    """Retourne la durée (s) d’un fichier MIDI – dépend de mido."""
    import mido
    mid = mido.MidiFile(mid_path)
    sec = sum(msg.time for msg in mid)  # temps absolu déjà en s
    return sec

def phasic_features(df: pd.DataFrame, sampling_rate: float) -> dict:
    """Calcule 10 métriques sur la composante phasique (NeuroKit)."""
    feats = {}
    phasic = df["EDA_Phasic"].values
    feats["max_phasic"]  = phasic.max()
    feats["area_phasic"] = np.trapz(phasic, dx=1/sampling_rate)
    peaks, _ = nk.signal_findpeaks(phasic, height=0.05)  # seuil 0,05 µS
    feats["nb_scr_peaks"] = len(peaks["Peaks"])
    if len(peaks["Peaks"]):
        feats["amp_peaks_sum"] = phasic[peaks["Peaks"]].sum()
    else:
        feats["amp_peaks_sum"] = 0.0
    # Ajouts tonique/brut
    feats["std_raw"]   = df["EDA_Raw"].std()
    feats["mean_raw"]  = df["EDA_Raw"].mean()
    feats["signal_len"] = len(df)
    # Pente tonique : régression linéaire simple
    y = df["EDA_Tonic"].values
    x = np.arange(len(df)) / sampling_rate
    slope = np.polyfit(x, y, 1)[0]
    feats["tonic_slope"] = slope
    feats["snr"] = (phasic.std() / df["EDA_Tonic"].std()) if df["EDA_Tonic"].std() else np.nan
    return feats

# ──────────────────────────────────────────────────────────────
# Boucle principale
# ──────────────────────────────────────────────────────────────
def main() -> None:
    args = parse_args()
    detections = pd.read_csv(args.detections_csv)

    merged_rows   = []
    feature_rows  = []

    for _, row in detections.iterrows():
        pid   = row["id_participant"]
        task  = row["task_type"].lower()          # perception / reproduction
        seq   = int(row["numero_sequence"])
        t0    = float(row["time_beginning"])
        tend  = (float(row["time_ending"])
                 if not math.isnan(row["time_ending"])
                 else t0 + midi_duration(args.midi_dir / f"{seq}.mid")
                 if args.midi_dir else np.nan)

        json_path = args.eda_dir / f"{pid}.json"
        if not json_path.exists():
            print(f"✖ Manquant : {json_path.name}")
            continue

        eda = load_json(json_path)
        # Fenêtre brute 64 Hz ⇒ décimation
        eda = eda[(eda["timestamp"] >= t0) & (eda["timestamp"] <= tend)].copy()
        if eda.empty:
            continue

        # Décimation à 4 Hz
        step = int(round(64 / args.resample))
        eda = eda.iloc[::step].reset_index(drop=True)
        eda["timestamp"] = eda["timestamp"] - t0  # t=0 au début

        # Décomposition : NeuroKit
        try:
            eda_proc, info = nk.eda_process(eda["eda_value"].values,
                                            sampling_rate=args.resample)
        except Exception as e:
            print(f"⚠ {pid} seq {seq}: {e}")
            continue
        df = pd.DataFrame(eda_proc)
        df["timestamp"] = eda["timestamp"]

        # Sauvegarde merged
        merged_rows.append(
            df.assign(id_participant=pid,
                      task_type=row["task_type"],
                      sequence_number=seq)
        )

        # Metriques
        feats = phasic_features(df, args.resample)
        feats.update(id_participant=pid,
                     task_type=row["task_type"],
                     sequence_number=seq)
        feature_rows.append(feats)

        # Plot
        out_png = args.plots_dir / pid / task / f"{seq}.png"
        out_png.parent.mkdir(parents=True, exist_ok=True)
        t = df["timestamp"]
        plt.figure(figsize=(10, 3))
        plt.plot(t, df["EDA_Raw"],    label="Raw",    lw=1)
        plt.plot(t, df["EDA_Tonic"],  label="Tonic",  lw=1)
        plt.plot(t, df["EDA_Phasic"], label="Phasic", lw=1)
        peaks = nk.signal_findpeaks(df["EDA_Phasic"], height=0.05)[0]["Peaks"]
        plt.scatter(t.iloc[peaks], df["EDA_Phasic"].iloc[peaks],
                    color="red", s=10, label="SCR Peaks")
        plt.title(f"{pid} – {row['task_type']} – séquence {seq}")
        plt.xlabel("Temps (s)")
        plt.ylabel("EDA (µS)")
        plt.tight_layout()
        plt.legend()
        plt.savefig(out_png, dpi=150)
        plt.close()
        print(f"✓ {out_png.relative_to(args.plots_dir)}")

    # Concat & export
    if merged_rows:
        pd.concat(merged_rows, ignore_index=True) \
          .to_csv(args.merged_csv, index=False)
        print(f"→ {args.merged_csv}")

    if feature_rows:
        pd.DataFrame(feature_rows) \
          .to_csv(args.features_csv, index=False)
        print(f"→ {args.features_csv}")

if __name__ == "__main__":
    main()
