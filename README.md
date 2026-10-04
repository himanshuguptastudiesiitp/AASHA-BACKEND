# 🌧️ AASHA Backend

### AI-Assisted Landslide Early Warning & Risk Monitoring System

> **AASHA** is the backend intelligence layer for an early-warning platform designed to monitor rainfall, soil moisture, rainfall trends, and accumulated precipitation to identify potentially high-risk landslide conditions across the **North Eastern Region (NER) of India**.

Built for **SIH 2026 — Problem Statement PS 26001**.

---

## 🚨 Why AASHA?

Landslides are rarely caused by a single rainfall event.

Risk can increase when:

* 🌧️ Current rainfall intensifies
* 💧 Soil moisture rises
* 📊 Short-term rainfall accumulates
* 📈 Rainfall trends become increasingly intense
* 🗓️ Antecedent rainfall builds up over several days

AASHA combines these signals into a **risk score and risk level** that can be consumed by a monitoring dashboard.

### Core Pipeline

```text
Weather Data
     ↓
Rainfall + Soil Moisture
     ↓
Temporal Rainfall Windows
     ↓
Trend Analysis
     ↓
Risk Scoring Engine
     ↓
Low / Moderate / High
     ↓
Alerts + Monitoring Dashboard
```

---

# ✨ Core Capabilities

| Capability                  | Description                                                   |
| --------------------------- | ------------------------------------------------------------- |
| 🌧️ Weather Ingestion       | Retrieves precipitation and soil-moisture data                |
| 💧 Soil Moisture Monitoring | Tracks near-surface soil moisture                             |
| 📊 Risk Scoring             | Computes a weighted landslide-risk score                      |
| 📈 Rainfall Trend           | Detects increasing, decreasing, or stable rainfall            |
| ⏱️ Multi-Window Analysis    | Evaluates 6h, 12h, 3d, 5d and 12d rainfall                    |
| 🗺️ NER Monitoring          | Provides risk information across representative NER locations |
| 🚨 Risk Alerts              | Generates actionable risk messages                            |
| 🔮 Forecast Risk            | Evaluates future rainfall and potential risk                  |
| 📍 High-Risk Zones          | Ranks monitored locations by risk score                       |
| 📋 Incident Reporting       | Allows users to submit field incidents                        |
| 📸 Evidence Upload          | Supports incident-related file uploads                        |
| 🗄️ Persistent Storage      | Stores rainfall, soil-moisture and incident data              |
| ⏰ Automated Refresh         | Periodically refreshes weather data                           |

The repository currently implements these capabilities through FastAPI endpoints and SQLAlchemy models.

---

# 🧠 Risk Assessment Engine

AASHA currently uses a **weighted rule-based risk engine**.

The score considers multiple environmental signals rather than relying only on current rainfall.

### Inputs

```text
Current Rainfall
       +
Soil Moisture
       +
Last 6 Hours Rainfall
       +
Last 12 Hours Rainfall
       +
Last 3 Days Rainfall
       +
Last 5 Days Rainfall
       +
Last 12 Days Rainfall
       +
Rainfall Trend
       ↓
Risk Score
```

### Risk Classification

|     Score | Risk Level  |
| --------: | ----------- |
|    `< 40` | 🟢 Low      |
| `40 – 69` | 🟠 Moderate |
|    `≥ 70` | 🔴 High     |

The current implementation assigns different weights to current rainfall, soil moisture, short-term accumulation, longer antecedent rainfall, and increasing rainfall trends.

> **Note:** This is currently a rule-based early-warning layer, not a clinically or scientifically validated landslide prediction model. Thresholds should be calibrated and validated against authoritative landslide observations before operational deployment.

---

# 🛰️ Weather Data Pipeline

AASHA currently integrates with **Open-Meteo** for hourly weather data.

The backend requests:

* Precipitation
* Soil moisture
* Historical rainfall
* Forecast rainfall
* Multiple geographic coordinates

The service uses the `Asia/Kolkata` timezone for weather processing.

### Automated Refresh

A background scheduler periodically refreshes weather information and stores newly observed records in the local database.

```text
Open-Meteo
     ↓
FastAPI Backend
     ↓
Risk Calculation
     ↓
SQLAlchemy
     ↓
SQLite
     ↓
Dashboard / API Consumers
```

---

# 🗺️ North Eastern Region Monitoring

AASHA includes representative monitoring points across the NER.

Currently configured locations include:

* Arunachal Pradesh
* Assam
* Manipur
* Meghalaya
* Mizoram
* Nagaland
* Sikkim
* Tripura

The `/risk-grid` endpoint evaluates these monitoring points and returns rainfall, soil moisture, rainfall trend, risk level and risk score.

---

# 📍 High-Risk Zone Monitoring

The backend also maintains a set of representative high-risk monitoring locations including:

* Tawang
* Cherrapunji
* Kohima
* Imphal
* Aizawl
* Gangtok
* Agartala
* Jorhat

Results are sorted by calculated risk score so that higher-priority locations can be surfaced first.

---

# 🔮 Forecast Risk Analysis

AASHA can evaluate forecast weather data and calculate risk for each forecast time step.

The `/rainfall/forecast-risk` endpoint returns:

```json
{
  "forecast": {
    "time": [],
    "rainfall": [],
    "soil_moisture": [],
    "risk_level": [],
    "risk_scores": []
  },
  "highest_risk": {
    "risk_level": "High",
    "risk_score": 75,
    "time": "..."
  }
}
```

This enables a frontend dashboard to visualize **when the highest forecasted risk may occur**.

---

# 🚨 Alert Generation

The backend converts calculated risk into human-readable alerts.

### High Risk

```text
ALERT: High landslide risk detected.
Immediate action required.
```

### Moderate Risk

```text
WARNING: Moderate landslide risk detected.
Continue monitoring.
```

### Low Risk

```text
No immediate landslide risk detected.
```

These messages are generated directly by the backend risk engine.

---

# 📋 Incident Reporting

AASHA also provides a field-level incident reporting system.

Users can submit:

* Name
* Role
* State
* Problem type
* Location
* Description
* Rating
* Feedback
* Supporting files/photos

Uploaded files are stored under the backend's `uploads/` directory and associated with the incident record.

### Incident Lifecycle

```text
Submitted
    ↓
Open
    ↓
Under Review
    ↓
Resolved
```

Supported statuses:

```text
Open
Under Review
Resolved
```

---

# 🏗️ Backend Architecture

```text
                    ┌──────────────────────┐
                    │     Frontend / GIS   │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │      FastAPI API     │
                    └──────────┬───────────┘
                               │
             ┌─────────────────┼─────────────────┐
             ▼                 ▼                 ▼
      Weather Service     Risk Engine      Incident API
             │                 │                 │
             ▼                 ▼                 ▼
        Open-Meteo       Risk Score        File Upload
             │                 │                 │
             └─────────────────┼─────────────────┘
                               ▼
                    ┌──────────────────────┐
                    │      SQLAlchemy      │
                    └──────────┬───────────┘
                               ▼
                    ┌──────────────────────┐
                    │        SQLite        │
                    └──────────────────────┘
```

---

# 🛠️ Tech Stack

### Backend

* **Python**
* **FastAPI**
* **Uvicorn**
* **SQLAlchemy**
* **SQLite**
* **Requests**
* **APScheduler**
* **python-multipart**

These dependencies are declared in the repository's `requirements.txt`.

### Data & Geospatial Assets

* Open-Meteo weather API
* GeoJSON state boundaries
* India state boundary data
* Assam geographic data

The repository currently contains `india-states-simplified.geojson` and `Assam.geojson`.

---

# 📁 Project Structure

```text
AASHA-BACKEND/
│
├── main.py
│   └── FastAPI application
│
├── models.py
│   └── SQLAlchemy database models
│
├── database.py
│   └── Database engine and session configuration
│
├── requirements.txt
│   └── Python dependencies
│
├── india-states-simplified.geojson
│   └── Simplified India state boundaries
│
├── Assam.geojson
│   └── Assam geographic data
│
├── gitignore.txt
│   └── Git ignore configuration
│
└── README.md
    └── Project documentation
```

The current repository contains the FastAPI application, database layer, SQLAlchemy models, dependencies and geographic assets listed above.

---

# ⚙️ Getting Started

## 1. Clone the Repository

```bash
git clone https://github.com/himanshuguptastudiesiitp/AASHA-BACKEND.git

cd AASHA-BACKEND
```

---

## 2. Create a Virtual Environment

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### Linux / macOS

```bash
python3 -m venv venv
source venv/bin/activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 4. Start the Backend

```bash
uvicorn main:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

---

# 📚 API Documentation

FastAPI automatically generates interactive API documentation.

### Swagger UI

```text
http://127.0.0.1:8000/docs
```

### ReDoc

```text
http://127.0.0.1:8000/redoc
```

---

# 🔌 API Endpoints

## 🌧️ Weather & Rainfall

| Method | Endpoint                  | Purpose                                      |
| ------ | ------------------------- | -------------------------------------------- |
| `GET`  | `/rainfall`               | Fetch rainfall and soil-moisture information |
| `GET`  | `/rainfall/history`       | Retrieve stored rainfall records             |
| `GET`  | `/rainfall/by-date`       | Analyze rainfall for a selected date         |
| `GET`  | `/rainfall/summary`       | Generate rainfall/risk summary               |
| `GET`  | `/rainfall/chart`         | Return recent rainfall chart data            |
| `GET`  | `/rainfall/forecast-risk` | Calculate forecast risk                      |

---

## 🚨 Risk & Monitoring

| Method | Endpoint           | Purpose                              |
| ------ | ------------------ | ------------------------------------ |
| `GET`  | `/test-risk`       | Test the risk engine                 |
| `GET`  | `/alerts`          | Generate current risk alert          |
| `GET`  | `/risk-grid`       | Monitor representative NER locations |
| `GET`  | `/high-risk-zones` | Rank monitored high-risk zones       |

---

## 💧 Soil Moisture

| Method | Endpoint                 | Purpose                               |
| ------ | ------------------------ | ------------------------------------- |
| `GET`  | `/soil-moisture/history` | Retrieve stored soil-moisture records |

---

## 📋 Incident Management

| Method | Endpoint                               | Purpose                |
| ------ | -------------------------------------- | ---------------------- |
| `POST` | `/incident-reports`                    | Submit an incident     |
| `GET`  | `/incident-reports`                    | Retrieve incidents     |
| `PUT`  | `/incident-reports/{report_id}/status` | Update incident status |

The incident endpoints support multipart form submission and optional file uploads.

---

# 🧪 Example API Calls

### Risk Test

```bash
curl http://127.0.0.1:8000/test-risk
```

### Rainfall Data

```bash
curl "http://127.0.0.1:8000/rainfall?latitude=27.586&longitude=91.859"
```

### Risk Summary

```bash
curl "http://127.0.0.1:8000/rainfall/summary?latitude=27.586&longitude=91.859"
```

### NER Risk Grid

```bash
curl http://127.0.0.1:8000/risk-grid
```

### High-Risk Zones

```bash
curl http://127.0.0.1:8000/high-risk-zones
```

---

# 🗄️ Database Design

AASHA currently uses **SQLite with SQLAlchemy**.

The database configuration points to:

```text
sih26001.db
```

The backend creates database tables through SQLAlchemy metadata initialization.

### Current Models

#### `Rainfall`

Stores:

* Latitude
* Longitude
* Timestamp
* Precipitation
* Unit
* Risk level
* Risk score

#### `SoilMoisture`

Stores:

* Latitude
* Longitude
* Timestamp
* Moisture
* Unit

#### `IncidentReport`

Stores:

* Reporter information
* State
* Problem type
* Location
* Description
* Uploaded evidence
* Rating
* Feedback
* Status
* Creation timestamp

The rainfall table also uses a uniqueness constraint across latitude, longitude and timestamp to reduce duplicate records.

---

# 🔐 Security & Production Considerations

This repository is currently positioned as a development/prototype backend.

Before production deployment, the following should be implemented:

* 🔑 API authentication
* 🛡️ Role-based authorization
* 🌐 Restricted CORS origins
* 🔒 HTTPS
* 📁 Secure file validation
* 📦 File size limits
* 🧹 Input validation
* 🗄️ Production database
* 🔐 Environment-based configuration
* 📊 Structured logging
* 🚦 API rate limiting
* 🧪 Automated tests
* 📈 Monitoring and observability

> **Important:** The current FastAPI configuration allows all CORS origins, so production deployments should replace this with an explicit allowlist.

---

# 🧭 Roadmap

### Phase 1 — Current Foundation

* [x] FastAPI backend
* [x] Weather API integration
* [x] Rainfall analysis
* [x] Soil-moisture analysis
* [x] Risk scoring
* [x] Risk alerts
* [x] NER monitoring grid
* [x] High-risk zone ranking
* [x] Forecast risk analysis
* [x] Incident reporting
* [x] Geographic assets

### Phase 2 — Advanced Intelligence

* [ ] Satellite imagery integration
* [ ] DEM / terrain features
* [ ] Slope and elevation analysis
* [ ] Historical landslide inventory
* [ ] Multi-source feature fusion
* [ ] ML-based risk prediction
* [ ] Model validation against historical events
* [ ] Spatial risk interpolation
* [ ] Dynamic risk thresholds

### Phase 3 — Operational Early Warning

* [ ] Real-time sensor integration
* [ ] District-level monitoring
* [ ] Automated alert escalation
* [ ] SMS / WhatsApp notifications
* [ ] Authority dashboard
* [ ] Alert acknowledgement workflow
* [ ] Audit logs
* [ ] Production cloud deployment

---

# 🎯 Vision

AASHA aims to evolve from a weather-driven risk scoring service into a **multi-source landslide early-warning backend**.

The long-term architecture can combine:

```text
Weather
   +
Soil Moisture
   +
Terrain / Slope
   +
Satellite Observations
   +
Historical Landslides
   +
Ground Sensors
   +
Rainfall Forecasts
        ↓
Multi-Source Risk Engine
        ↓
Spatial Risk Map
        ↓
Early Warning
        ↓
Authorities + Communities
```

The objective is not simply to show weather data.

> **The goal is to convert environmental signals into actionable early-warning intelligence.**

---

# 🤝 Contributing

Contributions are welcome.

### Development Flow

```bash
git clone <repository-url>

git checkout -b feature/your-feature

# Make your changes

git add .

git commit -m "feat: add your feature"

git push origin feature/your-feature
```

Then open a Pull Request describing:

* What changed
* Why it was needed
* How it was tested
* Any API changes
* Any database changes

---

# 📌 Project Status

**Status:** 🚧 Active Development

AASHA-BACKEND currently provides the core backend foundation for weather ingestion, environmental risk scoring, NER monitoring, forecast analysis and incident management.

The system should be considered a **prototype / development implementation** until its risk thresholds and predictions are validated against authoritative historical landslide observations.

---

# 👥 Team AASHA

**Smart India Hackathon 2026**

**Problem Statement:** PS 26001
**Theme:** Disaster Management
**Focus:** AI-assisted landslide early warning for the North Eastern Region of India

Built with the goal of turning fragmented environmental signals into timely, location-aware risk intelligence.

---

# 📜 License

This project currently does not specify an open-source license.

If this repository is intended to be publicly reusable, add an appropriate `LICENSE` file before declaring a license here.

---

## ⭐ Support the Project

If you find AASHA interesting:

* ⭐ Star the repository
* 🍴 Fork the project
* 🐛 Report issues
* 💡 Suggest improvements
* 🤝 Contribute to the project

---

### 🌄 AASHA

**Observe → Analyze → Assess → Alert**

> *From environmental data to early action.*
