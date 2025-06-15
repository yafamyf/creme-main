"""Association des temps de détection avec les données EDA."""

import argparse
import json
from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import neurokit2 as nk
from scipy import integrate
from scipy.stats import skew, kurtosis

try:
    import mido
except ImportError:
    mido = None


def midi_duration(midi_path: Path) -> float:
    """Return the duration of a MIDI file in seconds."""
    if mido is None:
        raise ImportError("mido library required to compute MIDI duration")
    m = mido.MidiFile(midi_path)
    return m.length


def load_detection_csv(path: Path) -> pd.DataFrame:
    """Load detection data from CSV and compute ending times if needed."""
    df = pd.read_csv(path)

    required = {"id_participant", "task_type", "numero_sequence", "time_beginning"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"Missing columns in detection CSV: {missing}")

    if "time_ending" not in df.columns:
        if "midi_file" not in df.columns:
            raise ValueError("CSV must contain either 'time_ending' or 'midi_file' column")

        durations = {}
        def compute_end(row):
            midi_path = Path(row["midi_file"])
            if midi_path not in durations:
                durations[midi_path] = midi_duration(midi_path)
            return row["time_beginning"] + durations[midi_path]

        df["time_ending"] = df.apply(compute_end, axis=1)

    return df


def load_eda_json(path: Path) -> pd.DataFrame:
    """Load EDA data from a JSON file."""
    with open(path) as f:
        data = json.load(f)
    start = data["timestampStart"]
    freq = data["samplingFrequency"]
    values = data["values"]
    timestamps = [start + i / freq for i in range(len(values))]
    df = pd.DataFrame({"timestamp": timestamps, "eda_value": values})
    df.attrs["sampling_rate"] = freq
    return df


def compute_features(values: pd.Series, sampling_rate: float) -> dict:
    """Return EDA phasic features for a signal."""
    signals, _ = nk.eda_process(values, sampling_rate=sampling_rate)
    phasic = signals["EDA_Phasic"]
    scr_amp = signals["SCR_Amplitude"]

    features = {
        "EDA Phasic Mean": float(np.mean(phasic)),
        "EDA Phasic Median": float(np.median(phasic)),
        "EDA Phasic STD": float(np.std(phasic)),
        "EDA Phasic Number of Peaks": int(signals["SCR_Peaks"].sum()),
        "EDA Phasic AUC": float(integrate.trapz(sorted(phasic), dx=1)),
        "EDA Phasic Max Amplitudes": float(np.nanmax(scr_amp)),
        "EDA Phasic Sum Amplitudes": float(np.nansum(scr_amp)),
        "EDA Phasic Mean Amplitudes": float(np.nanmean(scr_amp)),
        "EDA Phasic Kurtosis": float(kurtosis(phasic)),
        "EDA Phasic Skewness": float(skew(phasic)),
    }
    return features


def match_and_plot(
    detection_df: pd.DataFrame, eda_dfs: dict, out_dir: Path
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Create EDA plots for each sequence and return merged and feature data."""
    rows = []
    feature_rows = []
    for _, row in detection_df.iterrows():
        pid = str(row["id_participant"])
        task = row["task_type"]
        seq = row["numero_sequence"]
        t0 = row["time_beginning"]
        t1 = row["time_ending"]

        eda_df = eda_dfs[pid]
        window = eda_df[(eda_df["timestamp"] >= t0) & (eda_df["timestamp"] <= t1)]
        if window.empty:
            continue

        # compute features for this window
        feats = compute_features(window["eda_value"], eda_df.attrs["sampling_rate"])
        feats.update({"id_participant": pid, "task_type": task, "numero_sequence": seq})
        feature_rows.append(feats)

        # store rows for merged csv
        for _, r in window.iterrows():
            rows.append({
                "id_participant": pid,
                "numero_sequence": seq,
                "timestamp": r["timestamp"],
                "eda_value": r["eda_value"],
            })

        # plotting
        out_path = out_dir / pid / task / f"{seq}.png"
        out_path.parent.mkdir(parents=True, exist_ok=True)
        plt.figure(figsize=(10, 4))
        plt.plot(window["timestamp"], window["eda_value"], label="EDA")
        plt.xlabel("timestamp")
        plt.ylabel("EDA")
        plt.title(f"Participant {pid} - {task} seq {seq}")
        plt.tight_layout()
        plt.savefig(out_path)
        plt.close()

    return pd.DataFrame(rows), pd.DataFrame(feature_rows)


def main():
    parser = argparse.ArgumentParser(
        description="Match EDA data with detection times and compute features"
    )
    parser.add_argument("detection_csv", type=Path, help="CSV with detection times")
    parser.add_argument("eda_dir", type=Path, help="Directory containing EDA JSON files named <id_participant>.json")
    parser.add_argument("out_dir", type=Path, help="Output directory")
    parser.add_argument("output_csv", type=Path, help="Path to save merged CSV")
    parser.add_argument("features_csv", type=Path, help="Path to save features CSV")
    args = parser.parse_args()

    det_df = load_detection_csv(args.detection_csv)

    eda_dfs = {}
    for pid in det_df["id_participant"].unique():
        eda_path = args.eda_dir / f"{pid}.json"
        eda_dfs[pid] = load_eda_json(eda_path)

    merged, features = match_and_plot(det_df, eda_dfs, args.out_dir)
    merged.to_csv(args.output_csv, index=False)
    features.to_csv(args.features_csv, index=False)


if __name__ == "__main__":
    main()
