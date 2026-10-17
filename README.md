<div align="center">

# Water Data Streaming & Monitoring

**A Python-based pipeline for real-time data quality, anomaly analysis, and AI model monitoring.**

![Python](https://img.shields.io/badge/Python-3.9%2B-3776AB?logo=python&logoColor=white)
![Data Streaming](https://img.shields.io/badge/Data-Streaming-0A7EA4)
![Monitoring](https://img.shields.io/badge/Monitoring-Enabled-2E8B57)
![Status](https://img.shields.io/badge/Status-Active-brightgreen)
![License](https://img.shields.io/badge/License-MIT-blue)

</div>

---

## Table of Contents

- [Overview](#overview)
- [Key Features](#key-features)
- [Architecture](#architecture)
- [Technology Stack](#technology-stack)
- [Project Structure](#project-structure)
- [Results & Visualizations](#results--visualizations)
- [Getting Started](#getting-started)
- [Analytical Modules](#analytical-modules)
- [Data Management](#data-management)
- [Future Improvements](#future-improvements)
- [Disclaimer](#disclaimer)
- [License](#license)
- [Author](#author)

---

## Overview

**Water Data Streaming & Monitoring** is a Python-based project that simulates a real-time data pipeline for monitoring AI predictions in a water network environment.

The system generates streaming records, receives and validates incoming data, tracks data quality, and analyzes model performance over time.

The project demonstrates practical concepts in data engineering, streaming data processing, data quality validation, monitoring, and analytical reporting.

---

## Key Features

| Feature | Description |
|---|---|
| **Real-Time Data Streaming** | Simulates the continuous transmission of prediction records |
| **Data Validation** | Identifies malformed JSON records and invalid field values |
| **Data Quality Monitoring** | Tracks valid and invalid records and calculates error rates |
| **Model Performance Analysis** | Compares model response times and confidence scores |
| **Anomaly Analysis** | Analyzes unusual patterns in collected records |
| **Alert Analysis** | Summarizes monitoring alerts and their distribution across models |
| **Time-Series Analysis** | Examines monitoring metrics over time |
| **Data Visualization** | Generates charts for performance, confidence, errors, and alerts |

---

## Architecture

The project follows a streaming-and-analysis workflow:

```mermaid
flowchart TD
    A["Streaming Data Server<br/><code>water_ai_stream_server.py</code>"] -->|TCP / JSON| B["Data Receiver<br/><code>main.py</code>"]
    B --> C["Data Validation<br/><code>validator.py</code>"]
    C --> D["Data Storage & Monitoring<br/>CSV Records"]
    D --> E["Analysis & Reporting<br/>Performance · Anomalies · Alerts · Time Series"]
    E --> F["Charts & Dashboards"]
```

> **Note:** This diagram represents the intended workflow. The exact processing and storage behavior depends on the implementation of each module.

---

## Technology Stack

| Technology | Purpose |
|---|---|
| **Python** | Core implementation |
| **TCP Sockets** | Streaming communication |
| **JSON** | Data serialization and transmission |
| **CSV** | Record storage and analysis |
| **Pandas / NumPy** | Data processing, where used |
| **Matplotlib** | Visualization, where used |

---

## Project Structure

```text
Water-data-streaming-monitoring/
│
├── water_ai_stream_server.py
├── main.py
├── validator.py
│
├── alert_analysis.py
├── model_performance.py
├── model_performance_summary.py
├── summary_analysis.py
├── time_series_analysis.py
├── time_series_summary.py
│
├── dashboard.py
├── dashboard_data.py
├── time_series_dashboard.py
│
├── alert_summary.csv
├── anomaly_analysis.csv
├── anomaly_report.csv
├── model_performance_summary.csv
├── time_series_summary.csv
│
├── alerts_by_model.png
├── confidence_by_model.png
├── confidence_over_time.png
├── error_rate_over_time.png
├── response_time_by_model.png
├── response_time_over_time.png
│
├── .gitignore
└── README.md
```

---

## Results & Visualizations

The project includes visualizations for monitoring the quality and performance of streaming records.

### Error Rate Over Time

![Error Rate Over Time](error_rate_over_time.png)

### Response Time by Model

![Response Time by Model](response_time_by_model.png)

### Response Time Over Time

![Response Time Over Time](response_time_over_time.png)

### Confidence Scores by Model

![Confidence Scores by Model](confidence_by_model.png)

### Confidence Scores Over Time

![Confidence Scores Over Time](confidence_over_time.png)

### Alerts by Model

![Alerts by Model](alerts_by_model.png)

---

## Getting Started

### Prerequisites

- Python 3.9 or later
- Git
- The Python packages required by the project

### 1. Clone the Repository

```bash
git clone https://github.com/MahnooshB/Water-data-streaming-monitoring.git
cd Water-data-streaming-monitoring
```

### 2. Install Dependencies

Once the dependency file is available, install the required packages using:

```bash
pip install -r requirements.txt
```

### 3. Start the Streaming Server

Open a terminal and run:

```bash
python water_ai_stream_server.py
```

### 4. Start the Receiver

Open a second terminal and run:

```bash
python main.py
```

> The server and receiver are intended to run concurrently. Confirm that the receiver's connection settings match the server configuration before execution.

---

## Analytical Modules

| Module | Purpose |
|---|---|
| `alert_analysis.py` | Alert analysis |
| `model_performance.py` | Model performance analysis |
| `model_performance_summary.py` | Model performance summaries |
| `summary_analysis.py` | General analytical summaries |
| `time_series_analysis.py` | Time-series analysis |
| `time_series_summary.py` | Time-series summaries |
| `dashboard.py` | Dashboard functionality |
| `dashboard_data.py` | Dashboard data processing |
| `time_series_dashboard.py` | Time-series dashboard functionality |

---

## Data Management

Raw streaming records and files with `.pdf` and `.rar` extensions are excluded from version control through `.gitignore`.

The repository contains selected analytical outputs and visualizations. Before using the project with real infrastructure data, additional security, privacy, and operational controls would be required.

---

## Future Improvements

- [ ] Add automated unit and integration tests
- [ ] Document the data schema and validation rules
- [ ] Provide a reproducible Python environment
- [ ] Expand monitoring and anomaly detection capabilities
- [ ] Improve dashboard interactivity
- [ ] Add representative sample datasets
- [ ] Document measured throughput, latency, and data quality metrics
- [ ] Introduce continuous integration (CI)

---

## Disclaimer

> This project is intended for educational and portfolio purposes and uses simulated water-network data. It is **not** a production-ready water infrastructure monitoring system.

---

## License

This project is licensed under the MIT License.

See the [LICENSE](LICENSE) file for details.

---

## Author

**Mahnoosh Bagheri**

[![GitHub](https://img.shields.io/badge/GitHub-MahnooshB-181717?logo=github)](https://github.com/MahnooshB)
