# -*- coding: utf-8 -*-
"""
Created on Fri Sep 11 13:49:47 2026

@author: Mahnoosh
"""

import csv

ALERT_FILE = "alerts.csv"
SUMMARY_FILE = "alert_summary.csv"

model_stats = {}

with open(ALERT_FILE, "r", newline="", encoding="utf-8") as file:
     reader = csv.DictReader(file)
     for row in reader:
         model = row["model"]
         if model not in model_stats:
             model_stats[model] = {
                 "drift_alerts": 0,
                 "low_confidence_alerts": 0,
                 "total_alerts": 0,
                 "confidences": [],
                 "changes": []
                 }
         alert_type = row["alert_type"]
         model_stats[model]["total_alerts"] += 1
         
         if alert_type == "DRIFT":
             model_stats[model]["drift_alerts"] += 1
         elif alert_type == "LOW CONFIDENCE":
             model_stats[model]["low_confidence_alerts"] += 1
             
         confidence = float(row["confidence"])
         model_stats[model]["confidences"].append(confidence)
         
         if alert_type == "DRIFT":
             change = float(row["change_percent"])
             model_stats[model]["changes"].append(change)
             
with open(SUMMARY_FILE, "w", newline="", encoding="utf-8") as file:
    

    fieldnames = [
        "model",
        "drift_alerts",
        "low_confidence_alerts",
        "total_alerts",
        "avg_alert_confidence",
        "max_confidence_change"
    ]

    writer = csv.DictWriter(file, fieldnames = fieldnames)

    writer.writeheader()

    for model, stats in model_stats.items():
    
            avg_confidence = (sum(stats["confidences"])/ len(stats["confidences"]))
    
            if stats["changes"]:
                max_change = max(abs(change)for change in stats["changes"])
                
            else:
                max_change = 0

    writer.writerow({
                "model": model,
                "drift_alerts": stats["drift_alerts"],
                "low_confidence_alerts": stats["low_confidence_alerts"],
                "total_alerts": stats["total_alerts"],
                "avg_alert_confidence": round(avg_confidence, 3),
                "max_confidence_change": round(max_change, 2)
            })


print("Alert analysis completed.")

for model, stats in model_stats.items():
    print( model, "->", stats["total_alerts"], "alerts")
    


if __name__ == "__main__":
    ...
