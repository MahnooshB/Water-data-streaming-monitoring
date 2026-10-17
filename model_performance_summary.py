# -*- coding: utf-8 -*-
"""
Created on Fri Sep 18 22:00:45 2026

@author: Mahnoosh
"""
import csv


READINGS_FILE = "readings_clean.csv"
ALERTS_FILE = "alerts.csv"
OUTPUT_FILE = "model_performance_summary.csv"


def create_summary():

    model_stats = {}

    # -----------------------------
    # Read clean readings
    # -----------------------------
    with open(READINGS_FILE, "r", newline="", encoding="utf-8") as file:

        reader = csv.DictReader(file)

        for record in reader:

            model = record["model_name"]

            response_time = float(record["response_time_ms"])
            confidence = float(record["confidence_score"])

            if model not in model_stats:

                model_stats[model] = {
                    "records": 0,
                    "response_times": [],
                    "confidences": [],
                    "alerts": 0
                }

            model_stats[model]["records"] += 1
            model_stats[model]["response_times"].append(response_time)
            model_stats[model]["confidences"].append(confidence)


    # -----------------------------
    # Read alerts
    # -----------------------------
    with open(ALERTS_FILE, "r", newline="", encoding="utf-8") as file:

        reader = csv.DictReader(file)

        for alert in reader:

            model = alert["model"]

            if model in model_stats:
                model_stats[model]["alerts"] += 1


    # -----------------------------
    # Create summary CSV
    # -----------------------------
    fieldnames = [
        "model_name",
        "records",
        "average_response_time_ms",
        "minimum_response_time_ms",
        "maximum_response_time_ms",
        "average_confidence",
        "total_alerts"
    ]


    with open(
        OUTPUT_FILE,
        "w",
        newline="",
        encoding="utf-8"
    ) as file:

        writer = csv.DictWriter(
            file,
            fieldnames=fieldnames
        )

        writer.writeheader()


        for model, stats in model_stats.items():

            times = stats["response_times"]
            confidences = stats["confidences"]

            writer.writerow({
                "model_name": model,
                "records": stats["records"],
                "average_response_time_ms": round(
                    sum(times) / len(times), 2
                ),
                "minimum_response_time_ms": round(
                    min(times), 2
                ),
                "maximum_response_time_ms": round(
                    max(times), 2
                ),
                "average_confidence": round(
                    sum(confidences) / len(confidences), 2
                ),
                "total_alerts": stats["alerts"]
            })


    print("Model performance summary created successfully.")
    print("Output file:", OUTPUT_FILE)


if __name__ == "__main__":
    create_summary()
