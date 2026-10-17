# -*- coding: utf-8 -*-
"""
Created on Fri Sep 11 14:24:00 2026

@author: Mahnoosh
"""

import csv

ALERT_FILE = "alerts.csv"


def analyze_alerts():

    total_alerts = 0

    drift_alerts = 0
    low_confidence_alerts = 0

    model_alerts = {}

    with open(ALERT_FILE, "r", newline="", encoding="utf-8") as file:

        reader = csv.DictReader(file)

        for alert in reader:

            total_alerts += 1

            alert_type = alert["alert_type"]
            model = alert["model"]

            # Count alert type
            if alert_type == "DRIFT":
                drift_alerts += 1

            elif alert_type == "LOW CONFIDENCE":
                low_confidence_alerts += 1

            # Count alerts for each model
            if model not in model_alerts:
                model_alerts[model] = {
                    "total": 0,
                    "drift": 0,
                    "low_confidence": 0
                }

            model_alerts[model]["total"] += 1

            if alert_type == "DRIFT":
                model_alerts[model]["drift"] += 1

            elif alert_type == "LOW CONFIDENCE":
                model_alerts[model]["low_confidence"] += 1


    print("===================================")
    print("         ALERT ANALYSIS")
    print("===================================")

    print("Total Alerts:", total_alerts)
    print("Drift Alerts:", drift_alerts)
    print("Low Confidence Alerts:", low_confidence_alerts)

    print("-----------------------------------")

    for model in model_alerts:

        print("Model:", model)
        print("Total Alerts:", model_alerts[model]["total"])
        print("Drift Alerts:", model_alerts[model]["drift"])
        print(
            "Low Confidence Alerts:",
            model_alerts[model]["low_confidence"]
        )

        print("-----------------------------------")


if __name__ == "__main__":
    analyze_alerts()