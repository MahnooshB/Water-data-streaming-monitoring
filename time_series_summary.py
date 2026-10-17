# -*- coding: utf-8 -*-
"""
Created on Sat Sep 19 21:41:19 2026

@author: Mahnoosh
"""

import csv
from collections import defaultdict


READINGS_FILE = "readings_clean.csv"
BAD_READINGS_FILE = "bad_readings.csv"
OUTPUT_FILE = "time_series_summary.csv"


def load_valid_records():

    records = []

    with open(
        READINGS_FILE,
        "r",
        newline="",
        encoding="utf-8"
    ) as file:

        reader = csv.DictReader(file)

        for row in reader:
            records.append(row)

    return records


def load_invalid_records():

    records = []

    with open(
        BAD_READINGS_FILE,
        "r",
        newline="",
        encoding="utf-8"
    ) as file:

        reader = csv.DictReader(file)

        for row in reader:
            records.append(row)

    return records


def create_time_series():

    valid_records = load_valid_records()
    invalid_records = load_invalid_records()

    windows = defaultdict(
        lambda: {
            "valid": 0,
            "invalid": 0,
            "response_times": [],
            "confidence": []
        }
    )

    # -----------------------------
    # Valid records
    # -----------------------------

    for record in valid_records:

        timestamp = record["timestamp"]

        minute = timestamp[:16]

        # Ignore records with empty timestamp
        if not minute.strip():
            continue

        windows[minute]["valid"] += 1

        windows[minute]["response_times"].append(
            float(record["response_time_ms"])
        )

        windows[minute]["confidence"].append(
            float(record["confidence_score"])
        )

    # -----------------------------
    # Invalid records
    # -----------------------------

    for record in invalid_records:

        timestamp = record["timestamp"]

        minute = timestamp[:16]

        # Ignore records with empty timestamp
        if not minute.strip():
            continue

        windows[minute]["invalid"] += 1

    # -----------------------------
    # Create summary rows
    # -----------------------------

    summary = []

    for minute in sorted(windows):

        data = windows[minute]

        valid = data["valid"]
        invalid = data["invalid"]

        total = valid + invalid

        if total > 0:

            error_rate = (
                invalid / total
            ) * 100

        else:

            error_rate = 0

        if len(data["response_times"]) > 0:

            avg_response_time = (
                sum(data["response_times"])
                /
                len(data["response_times"])
            )

        else:

            avg_response_time = 0

        if len(data["confidence"]) > 0:

            avg_confidence = (
                sum(data["confidence"])
                /
                len(data["confidence"])
            )

        else:

            avg_confidence = 0

        summary.append({
            "timestamp": minute,
            "total_records": total,
            "valid_records": valid,
            "invalid_records": invalid,
            "error_rate_percent": round(error_rate, 2),
            "average_response_time_ms": round(
                avg_response_time,
                2
            ),
            "average_confidence": round(
                avg_confidence,
                2
            )
        })

    # -----------------------------
    # Save CSV
    # -----------------------------

    with open(
        OUTPUT_FILE,
        "w",
        newline="",
        encoding="utf-8"
    ) as file:

        fieldnames = [
            "timestamp",
            "total_records",
            "valid_records",
            "invalid_records",
            "error_rate_percent",
            "average_response_time_ms",
            "average_confidence"
        ]

        writer = csv.DictWriter(
            file,
            fieldnames=fieldnames
        )

        writer.writeheader()

        writer.writerows(summary)

    print(
        "Time-series summary created successfully."
    )

    print(
        "Output file:",
        OUTPUT_FILE
    )

    print(
        "Time windows:",
        len(summary)
    )


if __name__ == "__main__":
    create_time_series()