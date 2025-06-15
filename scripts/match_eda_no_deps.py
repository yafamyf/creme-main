#!/usr/bin/env python3
"""Merge detection windows with EDA values using only the standard library.

This script replicates :mod:`match_eda_by_timestamp.py` but avoids
third-party dependencies such as pandas and mido so that it can run in
minimal environments. It recursively scans a directory for Embrace JSON
exports, extracts EDA timestamps, and matches them with detection
intervals from ``detections.csv``.

The output directory will contain three CSV files:
- ``time_all_trials.csv`` with detection windows
- ``time_all_eda_values.csv`` with concatenated EDA values
- ``merged_eda_trials.csv`` with the final matching
"""

from __future__ import annotations

import argparse
import csv
import json
from bisect import bisect_left, bisect_right
from pathlib import Path
from typing import Iterable, List, Tuple

# ---------------------------------------------------------------------------
# Minimal MIDI duration parser
# ---------------------------------------------------------------------------

def _read_vlq(data: bytes, index: int) -> Tuple[int, int]:
    value = 0
    while True:
        b = data[index]
        index += 1
        value = (value << 7) | (b & 0x7F)
        if not (b & 0x80):
            break
    return value, index


def midi_duration(path: Path) -> float:
    """Return the duration of a MIDI file in seconds."""
    with path.open('rb') as f:
        data = f.read()
    if data[:4] != b'MThd':
        raise ValueError('Invalid MIDI header')
    ticks_per_quarter = int.from_bytes(data[12:14], 'big')
    if ticks_per_quarter & 0x8000:
        raise NotImplementedError('SMPTE time format not supported')
    index = 14
    ntracks = int.from_bytes(data[10:12], 'big')
    durations: List[float] = []
    for _ in range(ntracks):
        if data[index:index+4] != b'MTrk':
            raise ValueError('Invalid track header')
        length = int.from_bytes(data[index+4:index+8], 'big')
        track = data[index+8:index+8+length]
        index += 8 + length
        t = 0.0
        tempo = 500000  # default microseconds per quarter
        i = 0
        running_status = None
        while i < len(track):
            delta, i = _read_vlq(track, i)
            t += delta * tempo / ticks_per_quarter / 1_000_000
            status = track[i]
            if status & 0x80:
                i += 1
                running_status = status
            else:
                status = running_status
            if status == 0xFF:  # meta event
                meta_type = track[i]
                i += 1
                length, i = _read_vlq(track, i)
                meta_data = track[i:i+length]
                i += length
                if meta_type == 0x2F:
                    break
                if meta_type == 0x51 and length == 3:
                    tempo = (meta_data[0] << 16) | (meta_data[1] << 8) | meta_data[2]
            elif status in (0xF0, 0xF7):
                length, i = _read_vlq(track, i)
                i += length
            else:
                if running_status is None:
                    raise ValueError('Running status without prior status')
                if status & 0xF0 in (0xC0, 0xD0):
                    i += 1
                else:
                    i += 2
        durations.append(t)
    return max(durations) if durations else 0.0

# ---------------------------------------------------------------------------
# Loading helpers
# ---------------------------------------------------------------------------

def load_detection_csv(path: Path) -> List[dict]:
    rows: List[dict] = []
    with path.open(newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for r in reader:
            t0 = float(r['time_beginning'])
            midi = Path(r['midi_file'])
            t1 = t0 + midi_duration(midi)
            rows.append({
                'id_participant': r['id_participant'],
                'task_type': r['task_type'],
                'sequence_number': int(r['numero_sequence']),
                'time_beginning': t0,
                'time_ending': t1,
            })
    return rows


def load_eda_json(path: Path) -> List[Tuple[float, float]]:
    with path.open(encoding='utf-8') as f:
        data = json.load(f)
    if isinstance(data, list):
        data = data[0]
    if 'rawData' in data and 'eda' in data['rawData']:
        eda = data['rawData']['eda']
    elif 'eda' in data:
        eda = data['eda']
    else:
        raise KeyError('Cannot find EDA data in JSON')
    start = eda['timestampStart']
    if start > 1_000_000_000_000:
        start /= 1_000_000
    freq = eda['samplingFrequency']
    values = eda['values']
    return [(start + i / freq, float(val)) for i, val in enumerate(values)]


def load_all_eda_jsons(directory: Path) -> List[Tuple[float, float]]:
    values: List[Tuple[float, float]] = []
    for json_path in directory.rglob('*.json'):
        try:
            values.extend(load_eda_json(json_path))
        except Exception:
            continue
    values.sort(key=lambda x: x[0])
    return values

# ---------------------------------------------------------------------------
# Matching logic
# ---------------------------------------------------------------------------

def match_trials_with_eda(trials: List[dict], eda: List[Tuple[float, float]]) -> List[dict]:
    timestamps = [t for t, _ in eda]
    rows: List[dict] = []
    for t in trials:
        t0 = t['time_beginning']
        t1 = t['time_ending']
        start = bisect_left(timestamps, t0)
        end = bisect_right(timestamps, t1)
        for ts, val in eda[start:end]:
            rows.append({
                'id_participant': t['id_participant'],
                'sequence_number': t['sequence_number'],
                'timestamp': ts,
                'eda_value': val,
            })
    return rows

# ---------------------------------------------------------------------------
# CSV helpers
# ---------------------------------------------------------------------------

def write_csv(path: Path, fieldnames: Iterable[str], rows: Iterable[dict]) -> None:
    with path.open('w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)

# ---------------------------------------------------------------------------
# Main entry
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(description='Merge EDA values with detection times using timestamps only')
    parser.add_argument('detection_csv', type=Path, help='CSV with detection data')
    parser.add_argument('eda_dir', type=Path, help='Directory containing EDA JSON files')
    parser.add_argument('output_dir', type=Path, help='Directory to store CSV outputs')
    args = parser.parse_args()

    args.output_dir.mkdir(parents=True, exist_ok=True)

    trials = load_detection_csv(args.detection_csv)
    write_csv(
        args.output_dir / 'time_all_trials.csv',
        ['id_participant', 'task_type', 'sequence_number', 'time_beginning', 'time_ending'],
        trials,
    )

    eda_values = load_all_eda_jsons(args.eda_dir)
    write_csv(
        args.output_dir / 'time_all_eda_values.csv',
        ['timestamp', 'eda_value'],
        [{'timestamp': ts, 'eda_value': val} for ts, val in eda_values],
    )

    merged = match_trials_with_eda(trials, eda_values)
    write_csv(
        args.output_dir / 'merged_eda_trials.csv',
        ['id_participant', 'sequence_number', 'timestamp', 'eda_value'],
        merged,
    )


if __name__ == '__main__':
    main()
