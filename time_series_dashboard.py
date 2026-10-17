# -*- coding: utf-8 -*-
"""
Created on Sat Sep 19 23:48:26 2026

@author: Mahnoosh
"""

import csv
import matplotlib.pyplot as plt


INPUT_FILE = "time_series_summary.csv"


def create_charts():

    timestamps = []
    error_rates = []
    response_times = []
    confidences = []

    # -----------------------------
    # Read CSV
    # -----------------------------

    with open(
        INPUT_FILE,
        "r",
        newline="",
        encoding="utf-8"
    ) as file:

        reader = csv.DictReader(file)

        for row in reader:

            timestamps.append(row["timestamp"])

            error_rates.append(
                float(row["error_rate_percent"])
            )

            response_times.append(
                float(row["average_response_time_ms"])
            )

            confidences.append(
                float(row["average_confidence"])
            )


    print("Data loaded successfully.")
    print("Number of time windows:", len(timestamps))


    # =====================================
    # Chart 1 - Error Rate
    # =====================================

    plt.figure(figsize=(12, 6))

    plt.plot(
        timestamps,
        error_rates,
        marker="o"
    )

    plt.title("Error Rate Over Time")
    plt.xlabel("Time")
    plt.ylabel("Error Rate (%)")

    plt.xticks(
        rotation=45
    )

    plt.grid(True)

    plt.tight_layout()

    plt.savefig(
        "error_rate_over_time.png",
        dpi=150
    )

    plt.close()

    print(
        "Created: error_rate_over_time.png"
    )


    # =====================================
    # Chart 2 - Response Time
    # =====================================

    plt.figure(figsize=(12, 6))

    plt.plot(
        timestamps,
        response_times,
        marker="o"
    )

    plt.title(
        "Average Response Time Over Time"
    )

    plt.xlabel("Time")

    plt.ylabel(
        "Response Time (ms)"
    )

    plt.xticks(
        rotation=45
    )

    plt.grid(True)

    plt.tight_layout()

    plt.savefig(
        "response_time_over_time.png",
        dpi=150
    )

    plt.close()

    print(
        "Created: response_time_over_time.png"
    )


    # =====================================
    # Chart 3 - Confidence
    # =====================================

    plt.figure(figsize=(12, 6))

    plt.plot(
        timestamps,
        confidences,
        marker="o"
    )

    plt.title(
        "Average Confidence Over Time"
    )

    plt.xlabel("Time")

    plt.ylabel(
        "Average Confidence"
    )

    plt.xticks(
        rotation=45
    )

    plt.grid(True)

    plt.tight_layout()

    plt.savefig(
        "confidence_over_time.png",
        dpi=150
    )

    plt.close()

    print(
        "Created: confidence_over_time.png"
    )


    print()
    print("======================================")
    print("TIME-SERIES DASHBOARD COMPLETED")
    print("======================================")


if __name__ == "__main__":

    create_charts()