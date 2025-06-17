#!/usr/bin/env python3
"""
Pipeline EDA complet : scoring, filtrage, et génération de graphes.

Usage minimal (lancer depuis la racine du dépôt) :

    python scripts/eda_activity_scoring.py \
        scripts/eda_samples.csv \
        --report scripts/activity_report.csv \
        --keep   scripts/keep_sequences.csv \
        --plots  plots_active/ \
        --sampling-rate 4 \
        --peak-thr 1 \
        --amp-thr 0.05

Étapes réalisées :
1. **Scoring** de chaque séquence avec *neurokit2* → CSV `--report`
2. **Filtrage** : garde les séquences `nb_scr_peaks >= peak_thr` ET `max_phasic >= amp_thr` → CSV `--keep`
3. **Plotting** (Raw / Tonic / Phasic + pics) uniquement pour les séquences retenues → dossier `--plots`
4. Affiche un résumé : nombre total de séquences, % actives, top N listé au terminal.

Dépendances :
    pip install pandas neurokit2 matplotlib tqdm
"""

from __future__ import annotations

import argparse
import warnings
from pathlib import Path

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import neurokit2 as nk
from tqdm import tqdm

warnings.filterwarnings("ignore", category=UserWarning, module="neurokit2")

# ---------------------------------------------------------------------------
# ---------------------------   SCORING PART   ------------------------------
# ---------------------------------------------------------------------------

def score_sequence(signal: np.ndarray, sampling_rate: float) -> dict:
    """Retourne un dict de métriques objectives pour une séquence EDA."""
    if len(signal) < 10:
        return {
            "std_raw": np.nan,
            "max_phasic": np.nan,
            "area_phasic": np.nan,
            "nb_scr_peaks": 0,
            "signal_len": len(signal),
        }

    df, info = nk.eda_process(signal, sampling_rate=sampling_rate)
    phasic = df["EDA_Phasic"].values
    peaks = info.get("SCR_Peaks", [])

    return {
        "std_raw": float(np.std(signal)),
        "max_phasic": float(np.max(phasic)),
        "area_phasic": float(np.trapz(np.abs(phasic), dx=1 / sampling_rate)),
        "nb_scr_peaks": int(len(peaks)),
        "signal_len": int(len(signal)),
    }


def build_report(samples_csv: Path, sampling_rate: float) -> pd.DataFrame:
    df_samples = pd.read_csv(samples_csv)
    required = {"id_participant", "task_type", "sequence_number", "eda_value"}
    if not required.issubset(df_samples.columns):
        missing = required - set(df_samples.columns)
        raise ValueError(f"Colonnes manquantes dans {samples_csv}: {missing}")

    rows = []
    grouped = df_samples.groupby(["id_participant", "sequence_number", "task_type"])
    for (pid, seq, task), grp in tqdm(grouped, desc="Scoring séquences"):
        metrics = score_sequence(grp["eda_value"].values, sampling_rate)
        rows.append({
            "id_participant": pid,
            "sequence_number": seq,
            "task_type": task,
            **metrics,
        })
    return pd.DataFrame(rows)

# ---------------------------------------------------------------------------
# ---------------------------   PLOTTING PART   -----------------------------
# ---------------------------------------------------------------------------

def plot_sequence(signal: np.ndarray, sampling_rate: float, save_path: Path, title: str):
    df, info = nk.eda_process(signal, sampling_rate=sampling_rate)
    t = np.linspace(0, len(df) / sampling_rate, len(df))

    plt.figure(figsize=(10, 3))
    plt.plot(t, df["EDA_Raw"], label="Raw", linewidth=1)
    plt.plot(t, df["EDA_Tonic"], label="Tonic", linewidth=1)
    plt.plot(t, df["EDA_Phasic"], label="Phasic", linewidth=1)

    # pics SCR si dispos
    peaks_idx = info.get("SCR_Peaks", [])
    if len(peaks_idx):
        plt.scatter(t[peaks_idx], df["EDA_Phasic"].iloc[peaks_idx], color="red", s=15, zorder=5, label="SCR Peaks")

    plt.xlabel("Temps (s)")
    plt.ylabel("EDA (µS)")
    plt.title(title)
    plt.legend()
    plt.tight_layout()
    plt.savefig(save_path, dpi=150)
    plt.close()

# ---------------------------------------------------------------------------
# ---------------------------   MAIN PIPELINE   -----------------------------
# ---------------------------------------------------------------------------

def main():
    p = argparse.ArgumentParser(description="Scoring + filtrage + plotting EDA")
    p.add_argument("samples_csv", type=Path, help="eda_samples.csv")
    p.add_argument("--report", type=Path, default=Path("activity_report.csv"), help="CSV de sortie des scores")
    p.add_argument("--keep", type=Path, default=Path("keep_sequences.csv"), help="CSV des séquences retenues")
    p.add_argument("--plots", type=Path, default=None, help="Dossier où enregistrer les PNG (optionnel)")
    p.add_argument("--sampling-rate", type=float, default=4.0, help="Hz")
    p.add_argument("--peak-thr", type=int, default=1, help="seuil nb_scr_peaks")
    p.add_argument("--amp-thr", type=float, default=0.05, help="seuil max_phasic")
    p.add_argument("--top", type=int, default=20, help="afficher top N dans le terminal")
    args = p.parse_args()

    # 1. Scoring
    report = build_report(args.samples_csv, args.sampling_rate)
    report.to_csv(args.report, index=False)
    print(f"✓ rapport sauvegardé : {args.report}  ({len(report)} séquences)")

    # 2. Filtrage logique
    is_active = (report["nb_scr_peaks"] >= args.peak_thr) & (report["max_phasic"] >= args.amp_thr)
    kept = report[is_active].copy()
    kept.to_csv(args.keep, index=False)
    pct = 100 * len(kept) / len(report)
    print(f"✓ {len(kept)}/{len(report)} séquences actives  ({pct:.1f} %) → {args.keep}")

    # 3. Impression top N
    if args.top > 0:
        top = kept.sort_values(["nb_scr_peaks", "max_phasic"], ascending=False).head(args.top)
        print("\n>>> Top séquences (nb_scr_peaks, max_phasic):")
        for _, r in top.iterrows():
            print(f"  {r['id_participant']}  seq {int(r['sequence_number'])}  {r['task_type']}  »  peaks={r['nb_scr_peaks']}  amp={r['max_phasic']:.3f}")

    # 4. Plotting optionnel
    if args.plots is not None:
        print(f"\nGénération des PNG dans {args.plots} …")
        args.plots.mkdir(parents=True, exist_ok=True)

        df_samples = pd.read_csv(args.samples_csv)
        sel = set(zip(kept.id_participant, kept.sequence_number, kept.task_type))

        grouped = df_samples.groupby(["id_participant", "sequence_number", "task_type"])
        for (pid, seq, task), grp in tqdm(grouped, desc="Plotting", total=len(grouped)):
            if (pid, seq, task) not in sel:
                continue
            out_png = args.plots / pid / task.lower() / f"{int(seq)}.png"
            out_png.parent.mkdir(parents=True, exist_ok=True)
            title = f"{pid} – {task} – séquence {int(seq)}"
            plot_sequence(grp["eda_value"].values, args.sampling_rate, out_png, title)

        print("✓ plots terminés !\n")

if __name__ == "__main__":
    main()