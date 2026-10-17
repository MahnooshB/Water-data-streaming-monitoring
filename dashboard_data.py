# -*- coding: utf-8 -*-
"""
Created on Fri Sep 18 23:15:17 2026

@author: Mahnoosh
"""
import csv


READINGS_FILE = "readings_clean.csv"
BAD_READINGS_FILE = "bad_readings.csv"
ALERTS_FILE = "alerts.csv"


def count_records():

    valid_records = 0
    invalid_records = 0

    with open(
        READINGS_FILE,
        "r",
        newline="",
        encoding="utf-8"
    ) as file:

        reader = csv.DictReader(file)

        for _ in reader:
            valid_records += 1


    with open(
        BAD_READINGS_FILE,
        "r",
        newline="",
        encoding="utf-8"
    ) as file:

        reader = csv.DictReader(file)

        for _ in reader:
            invalid_records += 1


    return valid_records, invalid_records


def calculate_response_time():

    response_times = []

    with open(
        READINGS_FILE,
        "r",
        newline="",
        encoding="utf-8"
    ) as file:

        reader = csv.DictReader(file)

        for record in reader:

            response_times.append(
                float(record["response_time_ms"])
            )


    average = sum(response_times) / len(response_times)

    minimum = min(response_times)
    maximum = max(response_times)

    return average, minimum, maximum


def analyze_alerts():

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

        for alert in reader:

            total_alerts += 1

            if alert["alert_type"] == "DRIFT":
                drift_alerts += 1

            elif alert["alert_type"] == "LOW CONFIDENCE":
                low_confidence_alerts += 1


    return (
        total_alerts,
        drift_alerts,
        low_confidence_alerts
    )


def main():

    valid_records, invalid_records = count_records()

    total_records = valid_records + invalid_records

    error_rate = (
        invalid_records / total_records
    ) * 100


    average_time, minimum_time, maximum_time = (
        calculate_response_time()
    )


    total_alerts, drift_alerts, low_confidence_alerts = (
        analyze_alerts()
    )


    print("===================================")
    print("       SYSTEM PERFORMANCE")
    print("===================================")

    print("Total Records:", total_records)
    print("Valid Records:", valid_records)
    print("Invalid Records:", invalid_records)

    print("Error Rate:", round(error_rate, 2), "%")

    print(
        "Average Response Time:",
        round(average_time, 2),
        "ms"
    )

    print(
        "Minimum Response Time:",
        round(minimum_time, 2),
        "ms"
    )

    print(
        "Maximum Response Time:",
        round(maximum_time, 2),
        "ms"
    )

    print("-----------------------------------")

    print("Total Alerts:", total_alerts)
    print("Drift Alerts:", drift_alerts)
    print(
        "Low Confidence Alerts:",
        low_confidence_alerts
    )

    print("===================================")


if __name__ == "__main__":
    main()
