# -*- coding: utf-8 -*-
"""
Created on Wed Sep  9 21:24:32 2026

@author: Mahnoosh
"""
from datetime import datetime

REQUIRED_FIELDS = [
    "reading_id",
    "station_id",
    "model_name",
    "predicted_label",
    "confidence_score",
    "response_time_ms",
    "timestamp"
    ]

VALID_STATIONS = [
    "ST-01",
    "ST-02",
    "ST-03",
    "ST-04",
    "ST-05",
    "ST-06",
    "ST-07",
    "ST-08",
    "ST-09",
    "ST-10",
    ]

VALID_MODELS = {
    "leak_detector",
    "pressure_drop_predictor",
    "demand_forecaster"   
    }


VALID_LEAK_LABELS  = [
    "leak",
    "normal"
    ]

VALID_PRESSURE_LABELS = [
    "drop",
    "stable"
    ]

def validate_record(record):
    errors = []
    
    #1. Check Required Fields
    for field in REQUIRED_FIELDS:
        if field not in record:
            errors.append(f"{field} is missing") 
    
    #2. Check reading_id
    if "reading_id" in record:
        value = record["reading_id"]
        
        if type(value) is not int:
            errors.append("reading_id must be integer")
        elif value <= 0:
            errors.append("reading_id must be positive")
    
    #3. Check station_id        
    if "station_id" in record:
        value = record["station_id"]
        if value not in VALID_STATIONS:
            errors.append("station_id is invalid")
            
    #4. Check model_name & predicted_label       
    if "model_name" in record:
        value = record["model_name"]
        if value not in VALID_MODELS:
            errors.append("model_name is invalid")
        else:
            if "predicted_label" in record:
                if value == "leak_detector":
                    if record["predicted_label"] not in VALID_LEAK_LABELS:
                        errors.append("predicted_label is invalid for leak_detector")
                
                elif record["model_name"] == "pressure_drop_predictor":
                    if record["predicted_label"] not in VALID_PRESSURE_LABELS:
                        errors.append("predicted_label is invalid for pressure_drop_predictor")
                        
                elif record["model_name"] == "demand_forecaster":
                    value = record["predicted_label"]
                    if type(value) is not int:
                        errors.append("predicted_label must be integer for demand_forecaster")
                    elif not 1<= value <= 5000:
                            errors.append("predicted_label must be between 1 and 5000 for demand_forecaster")
    
    #5. Check confidence_score        
    if "confidence_score" in record:
        value = record["confidence_score"]
        
        if type(value) not in (int, float):
            errors.append("confidence_score must be a number")
        elif not 0<= value <= 1:
            errors.append("confidence_score must be between 0 and 1")
    
    #6. Check response_time_ms        
    if "response_time_ms" in record:
        value = record["response_time_ms"]
        
        if type(value) not in (int, float):
            errors.append("response_time_ms must be a number")
        elif  value <= 0:
            errors.append("response_time_ms must be positive")
            
    #7. Check timestamp       
    if "timestamp" in record:
        value = record["timestamp"]
        
        if type(value) is not str:
            errors.append("timestamp must be a string")
        else:
            try:
                datetime.strptime(value, "%Y-%m-%d %H:%M:%S.%f")
            except ValueError:
                errors.append("timestamp is invalid")
            
            
    return len(errors) == 0, errors


# if __name__ == "__main__":
#     records = {
#         "reading_id": -10,
#         "station_id": "ST-99",
#         "model_name": "unknown)model",
#         "predicted_label": "wrong",
#         "confidence_score": 1.5,
#         "response_time_ms": -20,
#         "timestamp": "wrong_date"}

#     valid, errors = validate_record(records)  

# print("valid: ", valid)   
# print("Errors: ", errors)
        