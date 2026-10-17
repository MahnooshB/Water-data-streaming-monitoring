# -*- coding: utf-8 -*-
"""
Created on Tue Sep  8 23:20:50 2026

@author: Mahnoosh
"""

import socket  #for TCP Connection
import json
import csv
import time
from validator import validate_record

#Server Properties:
HOST = "localhost"
PORT = 9034

CLEAN_FIELDNAMES = [
    "reading_id",
    "station_id",
    "model_name",
    "predicted_label",
    "confidence_score",
    "response_time_ms",
    "timestamp"
    ]

BAD_FIELDNAMES = CLEAN_FIELDNAMES + ["errors"]

ALERT_FIELDNAMES = [
    "alert_type",
    "model",
    "confidence",
    "baseline",
    "change_percent",
    "timestamp"
    ]

def receive_stream():
    
    total_records = 0
    valid_records = 0
    invalid_records = 0
    invalid_json = 0
    error_rate = 0
    last_report_records = 0
    # low_confidence = 0
    drift_threshold = 10
    low_confidence_threshold = 0.5
    run_duration = 120
    last_report_time = time.time()
    start_time = time.time()
    response_times = []
    alerts = []
    model_counts = {}
    model_response_times = {}
    model_confidence = {}
    window_model_counts = {}
    window_model_response_times = {}
    window_model_confidence = {}
    baseline_confidence = {}
    
    
    
    
    with open("readings_clean.csv", "a", newline="", encoding="utf-8") as clean_file, \
         open("bad_readings.csv", "a", newline="", encoding="utf-8") as bad_file, \
         open("alerts.csv", "a", newline="", encoding="utf-8") as alert_file:
            #Create CSV Writer
            clean_writer = csv.DictWriter(clean_file, fieldnames = CLEAN_FIELDNAMES)
            bad_writer = csv.DictWriter(bad_file, fieldnames = BAD_FIELDNAMES)
            alert_writer = csv.DictWriter(alert_file, fieldnames = ALERT_FIELDNAMES)

            #Check whether clean_file is empty 
            clean_file_empty = clean_file.tell() ==0
            #Write header if necessary
            if clean_file_empty:
                 clean_writer.writeheader()
                 
            bad_file_empty = bad_file.tell() ==0
            if bad_file_empty:
                bad_writer.writeheader()
                
            alert_file_empty = alert_file.tell() ==0
            if alert_file_empty:
                alert_writer.writeheader()
    
            with socket.create_connection((HOST, PORT)) as sock:
                buffer = ""
                
                while True:
                    current_time = time.time()
                    if current_time - start_time >= run_duration:
                        print("Maximum run duration reached.......")
                        break
                    data = sock.recv(4096)  # Max Received Byte: 4096
                    
                    if not data:
                        break
                    
                    buffer += data.decode("utf-8") # Transform Bytes to String and Add to the Buffer
                    
                    while "\n" in buffer: # Find a Complete Recoed
                        line, buffer = buffer.split("\n", 1)
                        
                        if not line.strip():
                            continue
                        
                        try:
                            record = json.loads(line) # Convert JSON to Dictionary
                            total_records += 1
    
                            valid, errors = validate_record(record) 
                            
                            if valid: #Write to reading_clean.csv
                                clean_writer.writerow(record)
                                clean_file.flush()
                                valid_records += 1
                                response_times.append(record["response_time_ms"])
                                model = record["model_name"]
                                if model not in model_counts:
                                    model_counts[model] = 0
                                    model_response_times[model] = []
                                    model_confidence[model] = []
                                    
                                model_counts[model] += 1
                                model_response_times[model].append(record["response_time_ms"])
                                model_confidence[model].append(record["confidence_score"])
                                # model_conf = record["confidence_score"]
                                # if model_conf < 0.5:
                                #     low_confidence += 1
                                if model not in window_model_counts: #20-sec window_metric
                                    window_model_counts[model] = 0
                                    window_model_response_times[model] = []
                                    window_model_confidence[model] = []
                                    
                                window_model_counts[model] += 1
                                window_model_response_times[model].append(record["response_time_ms"])
                                window_model_confidence[model].append(record["confidence_score"])
                                
                            else: #Write to bad_reading.csv
                                bad_record = record.copy()
                                bad_record["errors"] = "; ".join(errors)
                                bad_writer.writerow(bad_record)
                                bad_file.flush()
                                invalid_records += 1
                                
                                
                            
                        except json.JSONDecodeError: # for Defective Records
                            invalid_json += 1 
                            print("Invalid JSON: ", line)                       
                            
                            

                            

                        current_time = time.time()
                        
                        if current_time - last_report_time >= 20:
                            elapsed_time= current_time - last_report_time
                            records_in_window = total_records - last_report_records
                            if elapsed_time>0:
                                throughput = records_in_window/elapsed_time
                            else:
                                throughput = 0
                                
                            if (total_records + invalid_json) > 0:
                                error_rate = ((invalid_records + invalid_json) / (total_records + invalid_json)) * 100
                            else:
                                error_rate = 0
                            
                            if response_times:
                                avg_response_time = sum(response_times)/len(response_times)
                                min_response_time = min(response_times)
                                max_response_time = max(response_times)
                            else:
                                avg_response_time = 0
                                min_response_time = 0
                                max_response_time = 0
                            # print("---------20 Second Report---------")
                            # print("Total_Records: ", total_records)
                            # print("Valid_Records: ", valid_records)
                            # print("Invalid_Records: ", invalid_records)
                            # print("Invalid_Json: ", invalid_json)
                            # print("Error_Rate: ", round(error_rate, 2), "%")
                            # print("Throughput: ", round(throughput, 2), "records/sec")
                            # print("Average Response Time: ", round(avg_response_time, 2), "ms")
                            # print("Minimum Response Time: ", round(min_response_time, 2), "ms")
                            # print("Maximun Response Time: ", round(max_response_time, 2), "ms")
                            # print("-----------------------------------")
                            print("---------20 Second Window Metrics---------")
                            for model in model_counts:
                                times = model_response_times[model]
                                confidence = model_confidence[model]
                                avg_time = sum(times)/len(times)
                                avg_confidence = sum(confidence)/len(confidence)  
                            #     print("Model: ", model)
                            #     print("Records: ", model_counts[model])
                            #     print("Average Response Time: ", round(avg_time, 2), "ms")
                            #     print("Average Confidence: ", round(avg_confidence, 2))
                            #     # print("Low Confidence Quantity: ", low_confidence)
                            #     print("-----------------------------------")
                            
                            if not window_model_counts:
                                print("No Valid Records Found in this 20-sec Window")
                            else:
                            
                                for model in window_model_counts:
                                
                                    window_times = window_model_response_times[model]
                                    window_confidence = window_model_confidence[model]
                                
                                    avg_window_time = sum(window_times) / len(window_times)
                                    avg_window_confidence = sum(window_confidence) / len(window_confidence)
                                
                                    # Create baseline for the first window
                                    if model not in baseline_confidence:
                                        baseline_confidence[model] = avg_window_confidence
                                
                                    # Get baseline
                                    baseline = baseline_confidence[model]
                                
                                    # Calculate confidence change
                                    confidence_change = (
                                        (avg_window_confidence - baseline)
                                        / baseline
                                        * 100
                                    )
                                
                                    # Default status
                                    drift_status = "NORMAL"
                                
                                    # Drift Detection
                                    if abs(confidence_change) >= drift_threshold:
                                
                                        drift_status = "DRIFT DETECTED!"
                                
                                        alert = {
                                            "type": "DRIFT",
                                            "model": model,
                                            "confidence": round(avg_window_confidence, 2),
                                            "baseline": round(baseline, 2),
                                            "change_percent": round(confidence_change, 2)
                                        }
                                
                                        alerts.append(alert)
                                        alert_writer.writerow({
                                            "alert_type": "DRIFT",
                                            "model": model,
                                            "confidence": round(avg_window_confidence, 2),
                                            "baseline": round(baseline, 2),
                                            "change_percent": round(confidence_change, 2),
                                            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
                                            })
                                        alert_file.flush()
                                
                                        # print("!!! ALERT !!!")
                                        # print("DRIFT detected for:", model)
                                        # print("Confidence Change:", round(confidence_change, 2), "%")
                                
                                    # Low Confidence Detection
                                    if avg_window_confidence < low_confidence_threshold:
                                
                                        alert = {
                                            "type": "LOW CONFIDENCE",
                                            "model": model,
                                            "confidence": round(avg_window_confidence, 2)
                                        }
                                
                                        alerts.append(alert)
                                        alert_writer.writerow({
                                            "alert_type": "LOW CONFIDENCE",
                                            "model": model,
                                            "confidence": round(avg_window_confidence, 2),
                                            "baseline": round(baseline, 2),
                                            "change_percent": round(confidence_change, 2),
                                            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
                                            })
                                        alert_file.flush()
                                
                                    #     print("!!! ALERT !!!")
                                    #     print("LOW CONFIDENCE for:", model)
                                    #     print("Average Confidence:",
                                    #           round(avg_window_confidence, 2))
                                
                                    # # Print metrics
                                    # print("Model:", model)
                                    # print("Records:", window_model_counts[model])
                                    # print("Average Response Time:",
                                    #       round(avg_window_time, 2), "ms")
                                    # print("Average Confidence:",
                                    #       round(avg_window_confidence, 2))
                                    # print("Baseline Confidence:",
                                    #       round(baseline, 2))
                                    # print("Confidence Change:",
                                    #       round(confidence_change, 2), "%")
                                    # print("Drift Status:", drift_status)
                                    # print("-----------------------------------")
                                
                                
                                                              
                                last_report_time = current_time
                                last_report_records = total_records
                                response_times = []
                                # Reset Window metrics  
                                window_model_counts = {}
                                window_model_response_times = {}
                                window_model_confidence = {}
                            
                    
                        

    print("===========================================")
    print("            Final Summary              ") 
    print("===========================================")
    print("Total_Records: ", total_records)
    print("Valid_Records: ", valid_records)
    print("Invalid_Records: ", invalid_records)
    print("Invalid_Json: ", invalid_json)
        
    if (total_records + invalid_json) > 0:
        final_error_rate = ((invalid_records + invalid_json) / (total_records + invalid_json)) * 100
    else:
        final_error_rate = 0
        
    print("Final Error Rate: ", round(final_error_rate, 2))
    print("Total Alerts: ", len(alerts))
    print("===========================================")
    print("            Alert Summary              ") 
        
    drift_alert = 0
    low_confidence_alert = 0
        
    for alert in alerts:
        if alert["type"] == "DRIFT":
            drift_alert += 1
        elif alert["type"] == "LOW CONFIDENCE":
            low_confidence_alert += 1
        
    print("Drift Alerts: ", drift_alert)
    print("Low Confidence Alerts: ", low_confidence_alert)
    print("===========================================")

                            
if __name__ == "__main__":
    receive_stream()