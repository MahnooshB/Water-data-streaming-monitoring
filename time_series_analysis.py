# -*- coding: utf-8 -*-
"""
Created on Sat Sep 19 20:34:16 2026

@author: Mahnoosh
"""

import csv
from collections import defaultdict


READINGS_FILE = "readings_clean.csv"
BAD_READINGS_FILE = "bad_readings.csv"


def load_valid_records():

    records = []

    with open(READINGS_FILE, "r", newline="", encoding="utf-8") as file:

        reader = csv.DictReader(file)

        for row in reader:
            records.append(row)

    return records


def load_invalid_records():

    records = []

    with open(BAD_READINGS_FILE, "r", newline="", encoding="utf-8") as file:

        reader = csv.DictReader(file)

        for row in reader:
            records.append(row)

    return records


def analyze_by_minute():

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

    # --------------------------------
    # Valid records
    # --------------------------------

    for record in valid_records:

        timestamp = record["timestamp"]

        # Keep only year-month-day hour-minute
        minute = timestamp[:16]

        windows[minute]["valid"] += 1

        windows[minute]["response_times"].append(
            float(record["response_time_ms"])
        )

        windows[minute]["confidence"].append(
            float(record["confidence_score"])
        )


    # --------------------------------
    # Invalid records
    # --------------------------------

    for record in invalid_records:

        timestamp = record["timestamp"]

        minute = timestamp[:16]

        windows[minute]["invalid"] += 1


    # --------------------------------
    # Print time-series analysis
    # --------------------------------

    print("==========================================")
    print(" TIME-SERIES MONITORING")
    print("==========================================")


    for minute in sorted(windows):

        data = windows[minute]

        valid = data["valid"]
        invalid = data["invalid"]

        total = valid + invalid

        error_rate = (
            invalid / total
        ) * 100


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


        print()
        print("Time:", minute)

        print(
            "Total Records:",
            total
        )

        print(
            "Valid:",
            valid
        )

        print(
            "Invalid:",
            invalid
        )

        print(
            "Error Rate:",
            round(error_rate, 2),
            "%"
        )

        print(
            "Average Response Time:",
            round(
                avg_response_time,
                2
            ),
            "ms"
        )

        print(
            "Average Confidence:",
            round(
                avg_confidence,
                2
            )
        )

        print("------------------------------------------")


if __name__ == "__main__":
    analyze_by_minute()