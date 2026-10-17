# -*- coding: utf-8 -*-
"""
Created on Fri Sep 18 23:58:01 2026

@author: Mahnoosh
"""

import csv
import matplotlib.pyplot as plt


PERFORMANCE_FILE = "model_performance_summary.csv"
READINGS_FILE = "readings_clean.csv"
BAD_READINGS_FILE = "bad_readings.csv"
ALERTS_FILE = "alerts.csv"


# =========================================================
# 1. Load model performance data
# =========================================================

def load_model_performance():

    models = []
    response_times = []
    confidences = []
    alerts = []

    with open(
        PERFORMANCE_FILE,
        "r",
        newline="",
        encoding="utf-8"
    ) as file:

        reader = csv.DictReader(file)

        for row in reader:

            models.append(row["model_name"])

            response_times.append(
                float(row["average_response_time_ms"])
            )

            confidences.append(
                float(row["average_confidence"])
            )

            alerts.append(
                int(row["total_alerts"])
            )

    return models, response_times, confidences, alerts


# =========================================================
# 2. Calculate system KPIs
# =========================================================

def calculate_system_kpis():

    valid_records = 0
    invalid_records = 0
    response_times = []

    # -----------------------------
    # Read valid records
    # -----------------------------

    with open(
        READINGS_FILE,
        "r",
        newline="",
        encoding="utf-8"
    ) as file:

        reader = csv.DictReader(file)

        for row in reader:

            valid_records += 1

            response_times.append(
                float(row["response_time_ms"])
            )


    # -----------------------------
    # Read invalid records
    # -----------------------------

    with open(
        BAD_READINGS_FILE,
        "r",
        newline="",
        encoding="utf-8"
    ) as file:

        reader = csv.DictReader(file)

        for row in reader:

            invalid_records += 1


    # -----------------------------
    # Calculate KPIs
    # -----------------------------

    total_records = (
        valid_records +
        invalid_records
    )

    error_rate = (
        invalid_records /
        total_records
    ) * 100


    average_response_time = (
        sum(response_times) /
        len(response_times)
    )

    minimum_response_time = min(response_times)

    maximum_response_time = max(response_times)


    # -----------------------------
    # Count alerts
    # -----------------------------

    total_alerts = 0
    drift_alerts = 0
    low_confidence_alerts = 0

    with open(
        ALERTS_FILE,
        "r",
        newline="",
        encoding="utf-8"
    ) as file:

        reader = csv.DictReader(file)

        for row in reader:

            total_alerts += 1

            if row["alert_type"] == "DRIFT":
                drift_alerts += 1

            elif row["alert_type"] == "LOW CONFIDENCE":
                low_confidence_alerts += 1


    return {
        "total_records": total_records,
        "valid_records": valid_records,
        "invalid_records": invalid_records,
        "error_rate": error_rate,
        "average_response_time": average_response_time,
        "minimum_response_time": minimum_response_time,
        "maximum_response_time": maximum_response_time,
        "total_alerts": total_alerts,
        "drift_alerts": drift_alerts,
        "low_confidence_alerts": low_confidence_alerts
    }


# =========================================================
# 3. Print KPI dashboard
# =========================================================

def print_kpis(kpis):

    print()
    print("==========================================")
    print("          WATER AI MONITORING")
    print("              DASHBOARD")
    print("==========================================")

    print(
        "Total Records:",
        kpis["total_records"]
    )

    print(
        "Valid Records:",
        kpis["valid_records"]
    )

    print(
        "Invalid Records:",
        kpis["invalid_records"]
    )

    print(
        "Error Rate:",
        round(kpis["error_rate"], 2),
        "%"
    )

    print(
        "Average Response Time:",
        round(
            kpis["average_response_time"],
            2
        ),
        "ms"
    )

    print(
        "Minimum Response Time:",
        round(
            kpis["minimum_response_time"],
            2
        ),
        "ms"
    )

    print(
        "Maximum Response Time:",
        round(
            kpis["maximum_response_time"],
            2
        ),
        "ms"
    )

    print("------------------------------------------")

    print(
        "Total Alerts:",
        kpis["total_alerts"]
    )

    print(
        "Drift Alerts:",
        kpis["drift_alerts"]
    )

    print(
        "Low Confidence Alerts:",
        kpis["low_confidence_alerts"]
    )

    print("==========================================")


# =========================================================
# 4. Response Time Chart
# =========================================================

def plot_response_time(
    models,
    response_times
):

    plt.figure(figsize=(10, 6))

    plt.bar(
        models,
        response_times
    )

    plt.title(
        "Average Response Time by Model"
    )

    plt.xlabel("Model")

    plt.ylabel(
        "Average Response Time (ms)"
    )

    plt.xticks(
        rotation=15
    )

    plt.tight_layout()

    plt.savefig(
        "response_time_by_model.png",
        dpi=300
    )

    plt.show()


# =========================================================
# 5. Confidence Chart
# =========================================================

def plot_confidence(
    models,
    confidences
):

    plt.figure(figsize=(10, 6))

    plt.bar(
        models,
        confidences
    )

    plt.title(
        "Average Confidence by Model"
    )

    plt.xlabel("Model")

    plt.ylabel(
        "Average Confidence"
    )

    plt.ylim(
        0,
        1
    )

    plt.xticks(
        rotation=15
    )

    plt.tight_layout()

    plt.savefig(
        "confidence_by_model.png",
        dpi=300
    )

    plt.show()


# =========================================================
# 6. Alert Chart
# =========================================================

def plot_alerts(
    models,
    alerts
):

    plt.figure(figsize=(10, 6))

    plt.bar(
        models,
        alerts
    )

    plt.title(
        "Alerts by Model"
    )

    plt.xlabel("Model")

    plt.ylabel(
        "Number of Alerts"
    )

    plt.xticks(
        rotation=15
    )

    plt.tight_layout()

    plt.savefig(
        "alerts_by_model.png",
        dpi=300
    )

    plt.show()


# =========================================================
# Main
# =========================================================

def main():

    models, response_times, confidences, alerts = (
        load_model_performance()
    )

    kpis = calculate_system_kpis()

    print_kpis(kpis)

    plot_response_time(
        models,
        response_times
    )

    plot_confidence(
        models,
        confidences
    )

    plot_alerts(
        models,
        alerts
    )


if __name__ == "__main__":
    main()