# 🏔️ AASHA — Backend

## AI-Assisted Landslide Risk Intelligence & Early Warning Backend

<p align="center">

### 🌧️ Rainfall • 🌱 Soil Moisture • 📈 Temporal Accumulation • 🧠 Risk Scoring • 🚨 Alerts • 🗺️ NER Monitoring

</p>

<p align="center">

<img src="https://img.shields.io/badge/Project-AASHA-0A66C2?style=for-the-badge" alt="AASHA">

<img src="https://img.shields.io/badge/Domain-Disaster%20Management-E63946?style=for-the-badge" alt="Disaster Management">

<img src="https://img.shields.io/badge/Focus-Landslide%20Risk-F4A261?style=for-the-badge" alt="Landslide Risk">

<img src="https://img.shields.io/badge/Backend-FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white" alt="FastAPI">

<img src="https://img.shields.io/badge/Database-SQLAlchemy-CC2927?style=for-the-badge" alt="SQLAlchemy">

<img src="https://img.shields.io/badge/Status-Prototype%20%2F%20Research%20Build-6C757D?style=for-the-badge" alt="Prototype">

</p>

---

# ⚠️ PROPRIETARY SOFTWARE — ALL RIGHTS RESERVED

> **This repository is NOT open source.**

The source code, architecture, implementation logic, risk-scoring methodology, API implementation, data-processing logic, project-specific assets, and original materials contained in this repository are proprietary to the project owner(s).

### No license is granted to use this source code.

You may **view the repository for evaluation, academic review, demonstration, judging, or reference purposes**, but you are **not authorized** to:

- ❌ Copy the source code
- ❌ Reuse the implementation
- ❌ Fork the project for independent development
- ❌ Create derivative works
- ❌ Rebrand the system
- ❌ Reproduce the architecture
- ❌ Extract and reuse substantial portions of the implementation
- ❌ Use the code in another project
- ❌ Use the implementation commercially
- ❌ Redistribute modified or unmodified source code
- ❌ Publish the implementation elsewhere
- ❌ Package the backend as your own product
- ❌ Claim authorship or ownership of the implementation
- ❌ Train another system specifically from proprietary source implementation without permission

Any reuse beyond ordinary viewing of the public repository requires **explicit written permission from the copyright holder/project owner(s).**

> **No MIT, Apache-2.0, GPL, BSD, or other open-source license is granted by this repository.**

---

# 🏔️ AASHA

### **AI-Assisted Early Warning & Landslide Risk Intelligence System**

AASHA is a disaster-management technology initiative focused on transforming environmental observations into actionable landslide-risk intelligence.

The backend provides the computational and data layer for:

- 🌧️ Rainfall monitoring
- 🌱 Soil-moisture analysis
- 📊 Multi-timescale rainfall accumulation
- 📈 Rainfall trend analysis
- 🧠 Risk scoring
- 🚨 Risk alerts
- 🗺️ North Eastern Region monitoring
- 🔮 Forecast-based risk analysis
- 📍 High-risk-zone identification
- 📝 Incident reporting
- 📎 Incident evidence uploads
- 💾 Persistent environmental records

The system is designed around a fundamental principle:

> **A landslide-risk system should not look only at what is happening now. It should understand what has been accumulating before the current event.**

---

# 🎯 Vision

The long-term vision of AASHA is to build an intelligent early-warning ecosystem capable of combining:

```text
                    ENVIRONMENTAL DATA
                           │
          ┌────────────────┼────────────────┐
          │                │                │
          ▼                ▼                ▼
       Rainfall       Soil Moisture     Terrain
          │                │                │
          └────────────────┼────────────────┘
                           │
                           ▼
                TEMPORAL ANALYSIS
                           │
             ┌─────────────┼─────────────┐
             │             │             │
             ▼             ▼             ▼
          6 Hours       12 Hours     Multi-Day
             │             │             │
             └─────────────┼─────────────┘
                           ▼
                    RISK ENGINE
                           │
                           ▼
                 RISK SCORE + LEVEL
                           │
              ┌────────────┼────────────┐
              ▼            ▼            ▼
           LOW          MODERATE       HIGH
              │            │            │
              └────────────┼────────────┘
                           ▼
                    ALERT GENERATION
                           │
                           ▼
                 DECISION SUPPORT
🌍 Why This Backend Exists

Landslide susceptibility is influenced by multiple interacting factors.

A rainfall event cannot always be interpreted in isolation.

A slope that has experienced:

repeated rainfall,
increasing rainfall intensity,
elevated soil moisture,
significant accumulated precipitation,

may behave differently from an otherwise similar slope under dry antecedent conditions.

AASHA therefore introduces temporal rainfall accumulation into its current prototype risk engine.

The implementation evaluates rainfall over multiple temporal windows and combines these with soil-moisture and rainfall-trend signals.

🧠 Core Intelligence

The current backend implements a rule-based weighted risk engine.

It does not claim that the current prototype is a production-grade scientific landslide predictor.

Instead, it provides a computational framework that can later be calibrated and replaced/augmented with validated statistical and machine-learning models.

📊 Current Risk Engine

The backend evaluates several signals.

Immediate Rainfall

Current rainfall contributes to the risk score.

Current Rainfall
      │
      ├── Low
      ├── Moderate
      └── High
🌱 Soil Moisture

Soil moisture contributes another component to the risk score.

The current implementation uses the soil_moisture_0_to_1cm weather variable returned by the configured weather source.

⏱️ Short-Term Accumulation

The system calculates:

Last 6 Hours

Captures short-term rainfall accumulation.

Last 12 Hours

Captures a broader recent rainfall window.

📅 Antecedent Accumulation

The current implementation also evaluates:

Last 3 days
Last 5 days
Last 12 days

This allows the backend to distinguish a single isolated rainfall event from a prolonged wet period.

📈 Rainfall Trend

The system compares recent rainfall against a previous rainfall window.

Conceptually:

Previous 6 Hours
       │
       ▼
     COMPARE
       ▲
       │
Current 6 Hours
       │
       ▼
┌───────────────────┐
│ Trend             │
├───────────────────┤
│ Increasing        │
│ Decreasing        │
│ Stable            │
└───────────────────┘

The trend becomes another input to the combined risk calculation.

🧮 Combined Risk Score

The current implementation uses a weighted rule-based scoring approach.

Conceptually:

             CURRENT RAINFALL
                    │
                    ▼
             ┌─────────────┐
             │             │
SOIL ───────►│             │
MOISTURE     │  RISK       │
             │  ENGINE     │◄──── 6-HOUR RAINFALL
             │             │
12-HOUR ────►│             │
RAINFALL     │             │
             │             │◄──── 3-DAY RAINFALL
5-DAY ──────►│             │
RAINFALL     │             │
             │             │◄──── 12-DAY RAINFALL
TREND ──────►│             │
             └──────┬──────┘
                    │
                    ▼
               RISK SCORE
                    │
          ┌─────────┼─────────┐
          ▼         ▼         ▼
         LOW     MODERATE     HIGH

The current scoring implementation assigns weighted contributions to:

Current rainfall
Soil moisture
6-hour rainfall
12-hour rainfall
3-day accumulated rainfall
5-day accumulated rainfall
12-day accumulated rainfall
Rainfall trend

The resulting score is mapped to:

Score < 40
      ↓
LOW

40 ≤ Score < 70
      ↓
MODERATE

Score ≥ 70
      ↓
HIGH

The exact implementation is contained in the proprietary source code and should not be reproduced outside authorized use.

🚨 Alert Layer

Risk levels are converted into human-readable alerts.

LOW
No immediate landslide risk detected.
MODERATE
Moderate landslide risk detected.
Continue monitoring.
HIGH
High landslide risk detected.
Immediate action required.

The alert layer is intended as a decision-support component, not a substitute for official emergency authorities or validated operational warning systems.

🌧️ Weather Data Pipeline

The backend currently retrieves hourly environmental data from the configured weather API.

The implementation requests:

Precipitation
Soil moisture
Time
Location metadata

The current implementation uses Open-Meteo endpoints for forecast/archive data retrieval.

               LOCATION
                  │
                  ▼
          WEATHER API REQUEST
                  │
                  ▼
       ┌──────────────────────┐
       │ Hourly Environmental  │
       │ Data                  │
       ├──────────────────────┤
       │ Precipitation         │
       │ Soil Moisture         │
       │ Timestamp             │
       └──────────┬───────────┘
                  │
                  ▼
            AASHA ENGINE
                  │
          ┌───────┴───────┐
          ▼               ▼
       Database       Risk Engine
                          │
                          ▼
                   API Response
🔄 Automated Weather Refresh

The backend contains a background scheduler that refreshes weather information periodically.

The current implementation schedules the refresh process at an hourly interval.

        ┌─────────────────────┐
        │ Background Scheduler│
        └──────────┬──────────┘
                   │
              Every Hour
                   │
                   ▼
          Fetch Weather Data
                   │
                   ▼
         Calculate Risk Metrics
                   │
                   ▼
             Save to DB

This allows environmental data to be persisted for later retrieval.

🗄️ Database Layer

The backend uses SQLAlchemy as its ORM layer.

The current data model contains environmental and incident-report entities.

🌧️ Rainfall Model

The rainfall table stores:

ID
Latitude
Longitude
Timestamp
Precipitation
Unit
Risk level
Risk score

A uniqueness constraint is defined across:

latitude + longitude + timestamp

This helps prevent duplicate rainfall records for the same location and timestamp.

🌱 Soil Moisture Model

The soil-moisture table stores:

ID
Latitude
Longitude
Timestamp
Moisture
Unit
📝 Incident Report Model

Incident reports contain:

Reporter name
Reporter role
State
Problem type
Location
Description
Uploaded evidence references
Rating
Feedback
Status
Creation timestamp

Incident statuses currently include:

Open
   ↓
Under Review
   ↓
Resolved
📝 Incident Reporting

AASHA includes an incident-reporting workflow.

The backend supports:

User
 │
 ├── Name
 ├── Role
 ├── State
 ├── Problem Type
 ├── Location
 ├── Description
 ├── Rating
 ├── Feedback
 └── Evidence
          │
          ▼
   POST /incident-reports
          │
          ▼
       DATABASE
          │
          ▼
      Report ID
          │
          ▼
        Status

Uploaded files are stored in the backend's upload directory and exposed through the static upload route.

📎 Evidence Uploads

Incident reports can accept uploaded files.

The backend:

Receives multipart form data.
Processes uploaded files.
Generates unique stored filenames.
Saves them to the upload directory.
Stores their relative paths with the incident record.

This enables incident reports to carry supporting evidence.

🗺️ North Eastern Region Monitoring

AASHA contains a regional monitoring layer for the North Eastern Region of India.

The current backend defines representative monitoring points across:

Arunachal Pradesh
Assam
Manipur
Meghalaya
Mizoram
Nagaland
Sikkim
Tripura

These points can be processed through the risk engine to produce a regional risk grid.

                  NORTH EAST INDIA

                ┌───────────────────┐
                │ Arunachal Pradesh │
                └─────────┬─────────┘
                          │
       ┌──────────────────┼──────────────────┐
       ▼                  ▼                  ▼
    Assam             Nagaland           Sikkim
       │                  │                  │
       ▼                  ▼                  ▼
   Meghalaya           Manipur            Mizoram
       │
       ▼
    Tripura
🧭 Risk Grid

The /risk-grid endpoint evaluates representative monitoring points.

Each point can return:

State
Latitude
Longitude
Current rainfall
Soil moisture
Rainfall trend
Risk level
Risk score

Conceptually:

{
  "state": "Example State",
  "latitude": 00.0000,
  "longitude": 00.0000,
  "rainfall": 0.0,
  "soil_moisture": 0.0,
  "rainfall_trend": "Stable",
  "risk": "Low",
  "score": 0
}
🚨 High-Risk Zone Analysis

The backend also contains a high-risk-zone endpoint for predefined locations.

The current prototype includes representative locations such as:

Tawang
Cherrapunji
Kohima
Imphal
Aizawl
Gangtok
Agartala
Jorhat

Each location is evaluated using the risk engine and the results are sorted by risk score.

Locations
    │
    ▼
Weather Data
    │
    ▼
Risk Engine
    │
    ▼
Risk Score
    │
    ▼
Descending Sort
    │
    ▼
Highest-Risk Locations
🔮 Forecast Risk

AASHA provides a forecast-oriented risk endpoint.

The backend retrieves future hourly precipitation and soil-moisture values and applies the risk engine across the forecast horizon.

The output includes:

Forecast timestamps
Rainfall values
Soil-moisture values
Forecast risk levels
Forecast risk scores
Highest forecast risk
Time of highest predicted risk

Conceptually:

Forecast Horizon
       │
       ▼
Hourly Environmental Data
       │
       ▼
Risk Calculation
       │
       ├── Hour 1
       ├── Hour 2
       ├── Hour 3
       ├── ...
       └── Hour N
              │
              ▼
      Highest Risk Point
📊 Historical Rainfall

The backend supports historical rainfall retrieval.

Historical processing can calculate:

Total rainfall
Maximum hourly rainfall
Average hourly rainfall
6-hour accumulation
12-hour accumulation
3-day accumulation
5-day accumulation
12-day accumulation
Rainfall trend
Risk level
Risk score

This provides a basis for analyzing antecedent rainfall conditions.

📈 Rainfall Chart Data

A dedicated endpoint provides rainfall time-series data suitable for visualization.

The backend returns recent hourly timestamps and precipitation values.

This allows a frontend dashboard to render:

Rainfall
  │
  │          ╭──╮
  │      ╭───╯  ╰──╮
  │  ╭───╯         ╰──
  │──╯
  └──────────────────────── Time
🧩 API Surface

The current backend exposes several API capabilities.

Endpoint	Method	Purpose
/	GET	Backend health/message
/test-risk	GET	Test risk calculation
/rainfall	GET	Retrieve rainfall + soil-moisture analysis
/rainfall/history	GET	Retrieve stored rainfall records
/soil-moisture/history	GET	Retrieve stored soil-moisture records
/rainfall/by-date	GET	Historical date-specific rainfall analysis
/rainfall/summary	GET	Current rainfall/risk summary
/rainfall/chart	GET	Recent rainfall chart data
/alerts	GET	Current risk and alert information
/risk-grid	GET	NER representative monitoring grid
/high-risk-zones	GET	Ranked high-risk locations
/rainfall/forecast-risk	GET	Forecast-based risk analysis
/incident-reports	POST	Submit incident report
/incident-reports	GET	Retrieve incident reports
/incident-reports/{report_id}/status	PUT	Update incident status
🔌 Example API Requests
Current Risk Summary
GET /rainfall/summary?latitude=27.5860&longitude=91.8590
Alerts
GET /alerts?latitude=27.5860&longitude=91.8590
Rainfall Chart
GET /rainfall/chart?latitude=27.5860&longitude=91.8590
Forecast Risk
GET /rainfall/forecast-risk?latitude=27.5860&longitude=91.8590
Regional Risk Grid
GET /risk-grid
High-Risk Zones
GET /high-risk-zones
🏗️ Backend Architecture
                         AASHA
                           │
                           ▼
                    ┌─────────────┐
                    │   FastAPI   │
                    └──────┬──────┘
                           │
          ┌────────────────┼─────────────────┐
          │                │                 │
          ▼                ▼                 ▼
     Data Ingestion    Risk Engine      Incident API
          │                │                 │
          ▼                ▼                 ▼
     Weather API       Risk Score       File Upload
          │                │                 │
          └────────────────┼─────────────────┘
                           ▼
                    ┌─────────────┐
                    │ SQLAlchemy  │
                    └──────┬──────┘
                           │
                           ▼
                       Database
🛠️ Technology Stack
Backend
Python
FastAPI
Uvicorn
SQLAlchemy
Data & Integration
Requests
Open-Meteo API
JSON
Multipart file uploads
Scheduling
APScheduler
Geospatial Assets
GeoJSON
Database Abstraction
SQLAlchemy ORM
📁 Repository Structure
AASHA-BACKEND/
│
├── 📄 main.py
│   └── FastAPI application
│
├── 📄 models.py
│   └── SQLAlchemy data models
│
├── 📄 database.py
│   └── Database configuration
│
├── 📄 requirements.txt
│   └── Python dependencies
│
├── 🗺️ Assam.geojson
│   └── Assam geographic data
│
├── 🗺️ india-states-simplified.geojson
│   └── Simplified India state boundaries
│
├── 📄 gitignore.txt
│   └── Git ignore configuration
│
└── 📄 README.md
    └── Project documentation
⚙️ Requirements

The current dependency set includes:

fastapi
uvicorn[standard]
sqlalchemy
requests
apscheduler
python-multipart
🚀 Local Setup
1. Clone the repository
git clone https://github.com/himanshuguptastudiesiitp/AASHA-BACKEND.git
cd AASHA-BACKEND
2. Create a virtual environment
Windows
python -m venv venv
venv\Scripts\activate
Linux / macOS
python3 -m venv venv
source venv/bin/activate
3. Install dependencies
pip install -r requirements.txt
4. Start the backend
uvicorn main:app --reload

The backend will normally be available at:

http://127.0.0.1:8000
📚 Interactive API Documentation

FastAPI automatically provides interactive documentation.

After starting the server:

http://127.0.0.1:8000/docs

Alternative OpenAPI documentation:

http://127.0.0.1:8000/redoc

These interfaces can be used to inspect and test the API during authorized development.

🧪 Testing the Backend

After launching the server, test the health endpoint:

curl http://127.0.0.1:8000/

The backend should return a JSON response indicating that the SIH26001 backend is running.

🧠 Risk Engine Philosophy

The current prototype deliberately uses a transparent rule-based approach.

This offers several advantages during early development:

Explainability

Every risk score has identifiable contributing signals.

Debuggability

Thresholds can be inspected and adjusted.

Low Complexity

The prototype does not require a trained ML model to operate.

Easy Validation

Domain experts can review the logic before introducing more complex models.

🔬 Future Scientific Evolution

The current risk engine is a prototype decision-support mechanism.

A production-grade system should undergo extensive validation using:

Historical landslide inventories
Geological information
DEM-derived slope
Aspect
Elevation
Lithology
Land cover
Soil properties
Drainage characteristics
Historical rainfall
Soil-moisture observations
Satellite observations
Ground sensors
Official meteorological datasets

Future models may include:

Rule-Based Baseline
       ↓
Statistical Calibration
       ↓
Machine Learning
       ↓
Spatiotemporal Models
       ↓
Ensemble Risk Engine
🛰️ Future Data Sources

AASHA can be expanded to integrate additional environmental layers.

Potential sources include:

Meteorological observations
Satellite precipitation
Soil-moisture products
Digital Elevation Models
Geological maps
Landslide inventories
Ground sensors
Radar observations
Remote-sensing imagery

The objective is to move from:

Weather-only prototype
        ↓
Multi-source environmental intelligence
🗺️ Future Spatial Intelligence

The next generation of the platform can move beyond representative monitoring points.

Instead of:

8 Monitoring Points

the system could evolve toward:

        HIGH-RESOLUTION GRID

┌────┬────┬────┬────┬────┬────┐
│    │    │    │    │    │    │
├────┼────┼────┼────┼────┼────┤
│    │    │    │    │    │    │
├────┼────┼────┼────┼────┼────┤
│    │    │    │    │    │    │
├────┼────┼────┼────┼────┼────┤
│    │    │    │    │    │    │
└────┴────┴────┴────┴────┴────┘

Each Cell → Risk Score

This could eventually enable:

Slope-level monitoring
Village-level alerts
Road-corridor risk
Infrastructure risk
District-level dashboards
🚨 Future Early-Warning Pipeline

A mature AASHA architecture could evolve into:

┌──────────────────────────────────────────────┐
│                DATA SOURCES                  │
├──────────────────────────────────────────────┤
│ Rainfall • Radar • Satellite • Soil • DEM    │
│ Geology • Landslide Inventory • Sensors      │
└──────────────────────┬───────────────────────┘
                       │
                       ▼
              DATA INGESTION LAYER
                       │
                       ▼
             QUALITY CONTROL LAYER
                       │
                       ▼
             FEATURE ENGINEERING
                       │
                       ▼
            SPATIOTEMPORAL ENGINE
                       │
                       ▼
               RISK ENGINE
                       │
                       ▼
              CONFIDENCE LAYER
                       │
                       ▼
              ALERT GENERATION
                       │
             ┌─────────┼─────────┐
             ▼         ▼         ▼
          Dashboard  SMS/Alert  Authority
🧱 Engineering Principles
01. Explainability

Risk outputs should have understandable contributing factors.

02. Temporal Awareness

Recent rainfall should be interpreted together with antecedent conditions.

03. Data Integrity

Environmental observations should be stored consistently.

04. Modular Design

Weather ingestion, risk calculation, persistence and reporting should remain separable.

05. Extensibility

The prototype should be capable of evolving toward multi-source environmental intelligence.

06. Human Decision Support

The system should assist authorities and field users rather than claim autonomous emergency decision-making.

🔐 Security Considerations

The current repository is a prototype and should not automatically be treated as production-ready infrastructure.

Before production deployment, the following should be addressed:

Authentication
Authorization
Role-based access control
API rate limiting
Input validation
File-type validation
File-size restrictions
Malware scanning
Secure file storage
HTTPS
CORS restriction
Secret management
Database credential protection
Audit logging
Error sanitization
Monitoring
Backup and recovery
API abuse protection
⚠️ Important Production Security Note

The current development implementation contains permissive CORS configuration.

Before production deployment, this should be replaced with an explicit allowlist of trusted frontend origins.

Similarly, uploaded files should be subjected to stricter validation before any real-world deployment.

📡 Reliability Considerations

A production early-warning backend should account for:

API unavailable
     ↓
Retry
     ↓
Timeout
     ↓
Fallback
     ↓
Cached Data
     ↓
Data Freshness Check
     ↓
Risk Confidence

A risk system should never silently treat missing environmental data as trustworthy fresh data.

📊 Observability Roadmap

Future production deployments should monitor:

API
Request latency
Error rates
Throughput
Availability
Data
Data freshness
Missing observations
Duplicate observations
API failures
Risk Engine
Risk distribution
Score distribution
Threshold crossings
Model/logic drift
Alerts
Alert count
Alert delivery
False-alert analysis
Missed-event analysis
🧪 Validation Strategy

A serious landslide-risk system requires retrospective validation.

A possible framework:

Historical Weather
       +
Historical Landslide Events
       │
       ▼
Reconstruct Historical Conditions
       │
       ▼
Run AASHA Risk Engine
       │
       ▼
Compare Predictions vs Events
       │
       ▼
Evaluate
 ┌───────────────┐
 │ Precision      │
 │ Recall         │
 │ False Alarm    │
 │ Detection Lead │
 │ Reliability    │
 └───────────────┘

Only after appropriate validation should the system be considered for operational deployment.

📈 Future Performance Goals

Potential future engineering targets include:

Low-latency API responses
Efficient batch weather ingestion
Cached environmental datasets
Asynchronous processing
Background workers
Database indexing
Spatial indexing
API observability
Horizontal scaling
☁️ Future Deployment Architecture

A production architecture could evolve toward:

                    USERS
                      │
                      ▼
                LOAD BALANCER
                      │
                      ▼
                API GATEWAY
                      │
          ┌───────────┼───────────┐
          ▼           ▼           ▼
       API #1      API #2      API #N
          │           │           │
          └───────────┼───────────┘
                      ▼
                RISK SERVICES
                      │
          ┌───────────┼───────────┐
          ▼           ▼           ▼
       DATABASE      CACHE      QUEUE
          │           │           │
          └───────────┼───────────┘
                      ▼
                DATA SOURCES
🛣️ Development Roadmap
Phase 1 — Prototype
 FastAPI backend
 SQLAlchemy models
 Rainfall ingestion
 Soil-moisture ingestion
 Multi-window rainfall analysis
 Risk scoring
 Risk alerts
 Historical rainfall analysis
 Forecast risk
 NER risk grid
 High-risk zone analysis
 Incident reporting
 Evidence upload
Phase 2 — Data Engineering
 Automated data-quality checks
 Better caching
 Retry mechanisms
 Data freshness tracking
 Robust ingestion pipelines
 Structured logging
Phase 3 — Geospatial Intelligence
 High-resolution spatial grid
 DEM integration
 Slope calculation
 Aspect analysis
 Geological layers
 Landslide inventory integration
Phase 4 — AI / ML
 Historical-event dataset
 Feature engineering
 Model benchmarking
 Explainable ML
 Probability calibration
 Ensemble risk models
Phase 5 — Operational Early Warning
 Authority dashboards
 Notification infrastructure
 Alert escalation
 Multi-channel warnings
 Incident feedback loop
 Continuous validation
🌏 Long-Term Vision

AASHA aims to evolve from a prototype rainfall-risk backend into a comprehensive environmental intelligence platform.

TODAY

Rainfall
   +
Soil Moisture
   +
Temporal Windows
   ↓
Rule-Based Risk

↓

FUTURE

Rainfall
+
Radar
+
Satellite
+
Soil Moisture
+
DEM
+
Geology
+
Land Cover
+
Historical Landslides
+
Ground Sensors
+
Terrain Dynamics
        ↓
Spatiotemporal AI
        ↓
Probabilistic Risk
        ↓
Early Warning
🧭 Project Philosophy

AASHA is built around one core idea:

Early warning is not simply about detecting a trigger. It is about understanding the evolving condition of the environment before failure.

The backend therefore focuses on combining:

CURRENT CONDITIONS
        +
RECENT CONDITIONS
        +
ANTECEDENT CONDITIONS
        +
TREND
        ↓
BETTER RISK CONTEXT
⚠️ Scientific & Operational Disclaimer

AASHA is currently a prototype/research-oriented system.

Its risk scores and alerts should not be treated as official geological predictions, emergency warnings, evacuation orders, or authoritative disaster-management decisions.

The current rule-based thresholds are implementation-level prototype logic and require scientific calibration and validation before operational use.

For real-world deployment, the system would require validation against authoritative environmental datasets, historical landslide records, domain-expert review, reliability testing, security review and appropriate government/agency integration.

📜 Data & Third-Party Components

This project may interact with third-party data services and libraries.

Third-party software, APIs, datasets, maps and geographic assets remain subject to their respective licenses and terms.

The proprietary restriction in this repository applies to the original AASHA implementation, project-specific architecture, source code, original logic, and original project materials.

Third-party rights are not claimed by this notice.

🔒 Intellectual Property Notice
NO OPEN-SOURCE LICENSE

This repository intentionally does not grant an open-source license.

Copyright remains with the respective copyright holder(s).

You MAY:
View the repository.
Review the implementation for evaluation purposes.
Study the high-level project concept.
Reference the project appropriately in academic or judging contexts.
You MAY NOT without written permission:
Copy code.
Reuse code.
Fork for independent development.
Create derivative implementations.
Repackage the backend.
Commercialize the implementation.
Redistribute source code.
Publish copied sections.
Claim the implementation as your own.
Integrate substantial portions into another project.
Permission Requests

For authorized:

Collaboration
Licensing
Research use
Commercial use
Integration
Code reuse

please contact the project owner(s) directly.

🚫 No Warranty

The repository is provided as a prototype/research implementation.

No warranty is made regarding:

Accuracy
Availability
Reliability
Scientific validity
Operational readiness
Disaster prediction accuracy
Data completeness
Production security
🏆 Project Context

Project: AASHA
Domain: Disaster Management
Focus: Landslide Risk Monitoring & Early Warning
Region: North Eastern Region of India
Backend: FastAPI
Database Layer: SQLAlchemy
Environmental Data: Rainfall + Soil Moisture
Risk Engine: Rule-Based Weighted Scoring
Spatial Layer: GeoJSON + Representative NER Monitoring Points

👨‍💻 Repository

AASHA-BACKEND

https://github.com/himanshuguptastudiesiitp/AASHA-BACKEND
⭐ If You Are Evaluating This Project

This repository is intended to demonstrate:

Environmental data ingestion
Backend API engineering
Risk-scoring logic
Temporal rainfall analysis
Soil-moisture integration
Regional monitoring
Forecast-based risk analysis
Incident reporting
Geospatial data handling
Disaster-management system design

The source is publicly visible for transparency and evaluation, but visibility does not grant permission to reuse the implementation.

🔐 FINAL OWNERSHIP NOTICE
THIS CODE IS PROPRIETARY.
VIEWING ≠ PERMISSION TO USE.

The publication of this repository on GitHub does not constitute a grant of rights to copy, modify, distribute, sublicense, commercialize, or create derivative works from the source code.

All rights reserved.

<p align="center">
🏔️ AASHA
Observe. Understand. Anticipate. Act.

AI-Assisted Landslide Risk Intelligence

</p> <p align="center">

🌧️ Rainfall   •  
🌱 Soil Moisture   •  
📊 Risk Intelligence   •  
🗺️ Regional Monitoring   •  
🚨 Early Warning

</p> <p align="center">

Built with a focus on disaster resilience, environmental intelligence and responsible technology.

</p> ```
