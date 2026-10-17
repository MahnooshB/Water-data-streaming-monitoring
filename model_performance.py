# -*- coding: utf-8 -*-
"""
Created on Fri Sep 11 18:36:39 2026

@author: Mahnoosh
"""
import csv


READINGS_FILE = "readings_clean.csv"
ALERTS_FILE = "alerts.csv"


def load_model_performance():

    model_stats = {}

    # -----------------------------
    # Read valid readings
    # -----------------------------
    with open(READINGS_FILE,"r", newline="", encoding="utf-8") as file:

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

            model_stats[model]["response_times"].append(
                response_time
            )

            model_stats[model]["confidences"].append(
                confidence
            )


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
    # Print performance summary
    # -----------------------------
    print("===================================")
    print("       MODEL PERFORMANCE")
    print("===================================")

    for model in model_stats:

        stats = model_stats[model]

        times = stats["response_times"]
        confidences = stats["confidences"]

        avg_response_time = sum(times) / len(times)

        min_response_time = min(times)

        max_response_time = max(times)

        avg_confidence = sum(confidences) / len(confidences)

        print("Model:", model)

        print("Records:", stats["records"])

        print(
            "Average Response Time:",
            round(avg_response_time, 2),
            "ms"
        )

        print(
            "Minimum Response Time:",
            round(min_response_time, 2),
            "ms"
        )

        print(
            "Maximum Response Time:",
            round(max_response_time, 2),
            "ms"
        )

        print(
            "Average Confidence:",
            round(avg_confidence, 2)
        )

        print(
            "Total Alerts:",
            stats["alerts"]
        )

        print("-----------------------------------")


if __name__ == "__main__":
    load_model_performance()