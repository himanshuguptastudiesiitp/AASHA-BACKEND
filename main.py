from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import requests
from datetime import datetime, timedelta
import os
import shutil
import json
from apscheduler.schedulers.background import BackgroundScheduler

from database import engine, Base, SessionLocal
import models

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

os.makedirs("uploads", exist_ok=True)

app.mount(
    "/uploads",
    StaticFiles(directory="uploads"),
    name="uploads"
)

Base.metadata.create_all(bind=engine)

def calculate_risk(rainfall,soil_moisture):
    if rainfall > 5 and soil_moisture > 0.35:
        return "High"
    elif rainfall >2 or soil_moisture > 0.35:
        return "Moderate"
    else:
        return "Low"

def calculate_combined_risk(
        rainfall,
        soil_moisture,
        last_6_hours_rainfall,
        last_12_hours_rainfall,
        last_3_days_rainfall,
        last_5_days_rainfall,
        last_12_days_rainfall,
        rainfall_trend

):
    score=0

    # current rainfall =0
    if rainfall > 5:
        score += 15

    elif rainfall> 2:
        score +=8

    # soil moisture
    if soil_moisture > 0.35:
        score+=20
    elif soil_moisture > 0.25:
        score+=10

    # short-term rainfall
    if last_6_hours_rainfall > 10:
        score+=20
    elif last_6_hours_rainfall > 5:
        score+=10

    #12- hours rainfall
    if last_12_hours_rainfall > 20:
        score +=10
    elif last_12_hours_rainfall > 10:
        score +=5
    # 3 days accumulated rainfall
    if last_3_days_rainfall > 100:
        score +=10
    elif last_3_days_rainfall> 50:
        score +=5

    # 5 days accumulated rainfall

    if last_5_days_rainfall > 150:
        score +=5
    # 12 days accumulated rainfall
    if last_12_days_rainfall > 250:
        score+=5

    # rainfall trend
    if rainfall_trend == "Increasing":
        score+=10
    # risk classification 
    
    if score >=70:
        risk = "High"
    elif score >= 40 :
        risk = "Moderate"
    else:
        risk = "Low"

    return risk, score

def generate_alert(risk,risk_score):
    if risk =="High":
        return "ALERT: High landslide risk detected. Immediate action required ."
    elif risk=="Moderate":
        return "WARNING:  Moderate landslide risk detected. Continue monitoring."
    else:
        return "No immediate landslide risk detected."
    
def refresh_weather_data():

    latitude =26.0
    longitude= 85.0 
    url="https://api.open-meteo.com/v1/forecast"

    params={
        "latitude":latitude,
        "longitude":longitude,
        "hourly":"precipitation,soil_moisture_0_to_1cm",
        "forecast_days":12,
        "timezone":"Asia/Kolkata"
    }
    response = requests.get(url,params=params)
    data=response.json()

    db=SessionLocal()

    try:
        rainfall_values = data["hourly"]["precipitation"]
        soil_moisture_values=data["hourly"]["soil_moisture_0_to_1cm"]
        time_values=data["hourly"]["time"]

        for current_index,(time, rainfall, soil_moisture) in enumerate(
            zip(time_values, rainfall_values, soil_moisture_values

            )
        ):

        
        
            rainfall_record=models.Rainfall()


            rainfall_record.latitude=data["latitude"]
            rainfall_record.longitude=data["longitude"]

            
            rainfall_record.timestamp=datetime.fromisoformat(time)
            rainfall_record.precipitation = rainfall
            rainfall_record.unit=data["hourly_units"]["precipitation"]

            # last 6 hours rainfall
            last_6_hours_rainfall = sum(
                rainfall_values[max(0,current_index -5):current_index +1]
            )

            # previou 6 hours rainfall
            previous_6_hours_rainfall = sum(
                rainfall_values[max(0,current_index -11):current_index -5]
            )

            #last 12 hours rainfall
            last_12_hours_rainfall = sum(rainfall_values[
                max(0,current_index -11):current_index +1
            ])
            # last 3 days rainfall
            last_3_days_rainfall = sum(
                rainfall_values[max(0,current_index - 71):current_index +1]
            )

            # last 5 days rainfall
            last_5_days_rainfall = sum(
                rainfall_values[max(0,current_index -119):current_index +1]
            )
            # last 12 days rainfall
            last_12_days_rainfall=sum(
                rainfall_values[max(0,current_index - 287):current_index + 1]
            )

            # rainfall trend 
            if last_6_hours_rainfall > previous_6_hours_rainfall:
                rainfall_trend = "Increasing"
            elif last_6_hours_rainfall < previous_6_hours_rainfall:
                rainfall_trend = "Decreasing"
            else:
                rainfall_trend = "Stable"

            soil_moisture = soil_moisture if soil_moisture is not None else 0 


            risk,score= calculate_combined_risk(
                rainfall,
                soil_moisture,
                last_6_hours_rainfall,
                last_12_hours_rainfall,
                last_3_days_rainfall,
                last_5_days_rainfall,
                last_12_days_rainfall,
                rainfall_trend
            )

            rainfall_record.risk_level=risk
            rainfall_record.risk_score=score
            soil_data=models.SoilMoisture()

            soil_data.latitude=data["latitude"]
            soil_data.longitude=data["longitude"]
            soil_data.timestamp=datetime.fromisoformat(time)
            soil_data.moisture=soil_moisture
            soil_data.unit=data["hourly_units"]["soil_moisture_0_to_1cm"]

            existing_record =db.query(models.Rainfall).filter_by(
                latitude=data["latitude"],
                longitude=data["longitude"],
                timestamp=datetime.fromisoformat(time)
            ).first()

            if existing_record:
                continue

            db.add(rainfall_record)
            db.add(soil_data)



        db.commit()

        print("Weather data refreshed and saved to database.")

    finally:
        db.close()


scheduler=BackgroundScheduler()

scheduler.add_job(
    refresh_weather_data,
    "interval",
    hours=1
)

scheduler.start()



def calculate_risk_score(rainfall,soil_moisture):
    rainfall_score=min(rainfall*10,50)
    soil_score = min(soil_moisture*100,50)

    return rainfall_score+soil_score
    
    

@app.get("/test-risk")

def test_risk():
    rainfall = 6
    soil_moisture= 0.40
    last_6_hours_rainfall=12
    rainfall_trend="Increasing"

    risk,score = calculate_combined_risk(
        rainfall,
        soil_moisture,
        0,
        0,
        0,
        0,
        0,
        rainfall_trend
    )

    alert=generate_alert(risk,score)

    return{
        "rainfall":rainfall,
        "soil_moisture":soil_moisture,
        "last_6_hours_rainfall":last_6_hours_rainfall,
        "rainfall_trend":rainfall_trend,
        "risk":risk,
        "risk_score":score,
        "alert":alert
    }

@app.get("/")
def home():
    return{"message":"sih26001 backend is running. "}

@app.get("/rainfall")
def  get_rainfall(latitude:float,longitude:float):
    db=SessionLocal()

    try:
        url = "https://api.open-meteo.com/v1/forecast"

        params= {
            "latitude":latitude,
            "longitude": longitude,
            "hourly":"precipitation,soil_moisture_0_to_1cm",
            "forecast_days":1,
            "timezone":"Asia/Kolkata"
        }

        response = requests.get(url, params=params)
        data= response.json()

        rainfall_values= data["hourly"]["precipitation"]
        soil_moisture_values=data["hourly"]["soil_moisture_0_to_1cm"]
        time_values=data["hourly"]["time"]

        hourly_rainfall=data["hourly"]["precipitation"]
        hourly_soil_moisture=data["hourly"]["soil_moisture_0_to_1cm"]

        combined_risks=[]
        combined_scores=[]


        for time,rainfall, soil_moisture in zip(
            time_values,
            rainfall_values,
            soil_moisture_values
        ):

            rainfall_data= models.Rainfall()
            soil_data=models.SoilMoisture()

            rainfall_data.latitude = data["latitude"]
            rainfall_data.longitude = data["longitude"]
        
            rainfall_data.precipitation = rainfall

            soil_data.latitude=data["latitude"]
            soil_data.longitude=data["longitude"]
            soil_data.timestamp=datetime.fromisoformat(time)
            soil_data.moisture= soil_moisture
            soil_data.unit=data["hourly_units"]["soil_moisture_0_to_1cm"]

            current_index = time_values.index(time)

            # last 6 hours rainfall

            start_index = max(0,current_index -5)

            last_6_hours_rainfall = sum(
                hourly_rainfall[start_index:current_index + 1]
            )
            # previous 6 hours rainfall
            previous_start = max(0, current_index -11)
            previous_end= max(0, current_index -5)

            previous_6_hours_rainfall = sum(
                hourly_rainfall[previous_start:previous_end]
            )

            # last 12 hours rainfall
            last_12_hours_rainfall = sum(
                hourly_rainfall[
                    max(0,current_index - 11):current_index +1
                ]
            )

            # last 3 days rainfall 
            last_3_days_rainfall =sum(
                hourly_rainfall[
                    max(0,current_index - 71):current_index +1 
                ]
            )
            # last 5 days rainfall
            last_5_days_rainfall = sum(
                hourly_rainfall[
                    max(0,current_index -119):current_index +1
                ]
            )
            # last 12 days rainfall
            last_12_days_rainfall =sum(
                hourly_rainfall[
                    max(0,current_index -287):current_index +1
                ]
            )

            #Rainfall trend
            if last_6_hours_rainfall> previous_6_hours_rainfall:
                rainfall_trend = "Increasing"
            elif last_6_hours_rainfall < previous_6_hours_rainfall:
                rainfall_trend = "Decreasing "
            else:
                rainfall_trend = "Stable"

            # Combined risk 
            risk,combined_score = calculate_combined_risk(
                rainfall, 
                soil_moisture,
                last_6_hours_rainfall,
                last_12_hours_rainfall,
                last_3_days_rainfall,
                last_5_days_rainfall,
                last_12_days_rainfall,
                rainfall_trend
            )

            
            rainfall_data.risk_level = risk
            rainfall_data.risk_score=combined_score

            combined_risks.append(risk)
            combined_scores.append(combined_score)



            rainfall_data.unit = data["hourly_units"]["precipitation"]
            rainfall_data.timestamp = datetime.fromisoformat(time)

            existing_record=db.query(models.Rainfall).filter_by(
                latitude=data["latitude"],
                longitude=data["longitude"],
                timestamp=datetime.fromisoformat(time)
            ).first()

            if existing_record:
                soil_existing=db.query(models.SoilMoisture).filter_by(
                    latitude=data["latitude"],
                    longitude=data["longitude"],
                    timestamp=datetime.fromisoformat(time)
                ).first()

                if not soil_existing:
                    db.add(soil_data)

                continue

            db.add(rainfall_data)
            db.add(soil_data)


        db.commit()

        return {
            "location":{
                "latitude":data["latitude"],
                "longitude":data["longitude"],
                "elevation" :  data["elevation"]
            },
            "timezone":data["timezone"],
            "hourly_rainfall":{
                "time":data["hourly"]["time"],
                "precipitation": data["hourly"]["precipitation"],
                "unit":data["hourly_units"]["precipitation"],

                "risk_level":combined_risks,
                "risk_score":combined_scores,

                "soil_moisture":data["hourly"]["soil_moisture_0_to_1cm"]


            }
        }
    finally:
        db.close()
@app.get("/rainfall/history")
def rainfall_history():
    db = SessionLocal()
    rainfall_records = db.query(models.Rainfall).all()
    db.close()
    return rainfall_records

@app.get("/soil-moisture/history")
def soil_moisture_history():
    db=SessionLocal()
    soil_records=db.query(models.SoilMoisture).all()
    db.close()
    return soil_records

@app.get("/rainfall/by-date")
def rainfall_by_date(
    latitude: float,
    longitude: float,
    date: str
):
    url = "https://archive-api.open-meteo.com/v1/archive"

    params = {
        "latitude": latitude,
        "longitude": longitude,
        "start_date": (
            datetime.fromisoformat(date) - timedelta(days=12)
        ).strftime("%Y-%m-%d"),
        "end_date": date,
        "hourly": "precipitation",
        "timezone": "Asia/Kolkata"
    }

    response = requests.get(url, params=params)
    response.raise_for_status()

    data = response.json()

    rainfall_values = data["hourly"]["precipitation"]

    time_values=data["hourly"]["time"]

    target_index=None

    for i, time in enumerate(time_values):
        if time.startswith(date):
            target_index=i
            break

    if target_index is None:
        return{
            "Error":"Requests date data not available"
        }

    daily_rainfall = [
    value for value in rainfall_values[target_index:target_index + 24]
    if value is not None
    ]

    total_rainfall = sum(daily_rainfall)

    max_rainfall = max(daily_rainfall) if daily_rainfall else 0

    average_rainfall = (
        total_rainfall / len(daily_rainfall)
        if daily_rainfall
        else 0
    )

    # Rainfall windows for requested date

    last_6_hours_rainfall = sum(
        value for value in rainfall_values[
            max(0,target_index-5):target_index + 1
        ]
        if value is not None
    )

    last_12_hours_rainfall = sum(
        value for value in rainfall_values[
            max(0,target_index - 11):target_index +1
        ]
        if value is not None
    )
    last_3_days_rainfall = sum(
        value for value in rainfall_values[
            max(0,target_index - 71):target_index + 1
        ]
        if value is not None
    )
    last_5_days_rainfall = sum(
        value for value in rainfall_values[
            max(0,target_index - 119):target_index + 1
        ]
        if value is not None
    )

    last_12_days_rainfall=sum(
        value for value in rainfall_values[
            max(0,target_index - 287):target_index + 1
        ]
        if value is not None

    )

# Rainfall trend for requested date

    first_half = sum(
        value for value in daily_rainfall[:12]
        if value is not None
    )

    second_half = sum(
        value for value in daily_rainfall[12:24]
        if value is not None
    )

    if second_half > first_half:
        rainfall_trend = "Increasing"
    elif second_half < first_half:
        rainfall_trend = "Decreasing"
    else:
        rainfall_trend = "Stable"


    # Risk calculation
    risk, risk_score = calculate_combined_risk(
        rainfall=max_rainfall,
        soil_moisture=0,
        last_6_hours_rainfall=last_6_hours_rainfall,
        last_12_hours_rainfall=last_12_hours_rainfall,

        last_3_days_rainfall=last_3_days_rainfall,
        last_5_days_rainfall=last_5_days_rainfall,
        last_12_days_rainfall=last_12_days_rainfall,
        rainfall_trend=rainfall_trend
    )

    return {
        "latitude": latitude,
        "longitude": longitude,
        "date": date,
        "total_rainfall": total_rainfall,
        "max_hourly_rainfall": max_rainfall,
        "average_hourly_rainfall": average_rainfall,
        "last_6_hours_rainfall":last_6_hours_rainfall,
        "last_12_hours_rainfall":last_12_hours_rainfall,
        "last_3_days_rainfall":last_3_days_rainfall,
        "last_5_days_rainfall":last_5_days_rainfall,
        "last_12_days_rainfall":last_12_days_rainfall,
        "rainfall_trend": rainfall_trend,
        "risk_level": risk,
        "risk_score": risk_score,
        "unit": data["hourly_units"]["precipitation"]
    }
@app.get("/rainfall/summary")
def rainfall_summary(latitude: float, longitude: float):

    url = "https://api.open-meteo.com/v1/forecast"

    params = {
        "latitude": latitude,
        "longitude": longitude,
        "hourly": "precipitation,soil_moisture_0_to_1cm",
        "past_days": 12,
        "forecast_days": 1,
        "timezone": "Asia/Kolkata"
    }

    response = requests.get(url, params=params)

    if not response.ok:
        return {
            "error": "Weather data could not be fetched"
        }

    data = response.json()


    rainfall_values = data["hourly"]["precipitation"]

    soil_moisture_values = data["hourly"]["soil_moisture_0_to_1cm"]

    time_values = data["hourly"]["time"]


    # Current hour
    current_time = datetime.now().strftime("%Y-%m-%dT%H:00")

    # Find current hour index
    current_index = time_values.index(current_time)


    latest_rainfall = rainfall_values[current_index]

    latest_soil_moisture = soil_moisture_values[current_index]

    if latest_rainfall is None:
        latest_rainfall = 0

    if latest_soil_moisture is None:
        latest_soil_moisture = 0


    # ================= 6 HOURS =================

    start_6 = max(0, current_index - 5)

    last_6_hours_rainfall = sum(
        value or 0
        for value in rainfall_values[start_6:current_index + 1]
    )


    # ================= PREVIOUS 6 HOURS =================

    previous_start = max(0, current_index - 11)

    previous_end = max(0, current_index - 5)

    previous_6_hours_rainfall = sum(
        value or 0
        for value in rainfall_values[previous_start:previous_end]
    )


    # ================= 12 HOURS =================

    start_12 = max(0, current_index - 11)

    last_12_hours_rainfall = sum(
        value or 0
        for value in rainfall_values[start_12:current_index + 1]
    )


    # ================= 3 DAYS =================

    start_3_days = max(0, current_index - 71)

    last_3_days_rainfall = sum(
        value or 0
        for value in rainfall_values[start_3_days:current_index + 1]
    )


    # ================= 5 DAYS =================

    start_5_days = max(0, current_index - 119)

    last_5_days_rainfall = sum(
        value or 0
        for value in rainfall_values[start_5_days:current_index + 1]
    )


    # ================= 12 DAYS =================

    start_12_days = max(0, current_index - 287)

    last_12_days_rainfall = sum(
        value or 0
        for value in rainfall_values[start_12_days:current_index + 1]
    )


    # ================= RAINFALL TREND =================

    if last_6_hours_rainfall > previous_6_hours_rainfall:

        rainfall_trend = "Increasing"

    elif last_6_hours_rainfall < previous_6_hours_rainfall:

        rainfall_trend = "Decreasing"

    else:

        rainfall_trend = "Stable"


    # ================= TOTAL / AVERAGE / MAX =================

    rainfall_period = [
        value or 0
        for value in rainfall_values[start_12_days:current_index + 1]
    ]

    total_rainfall = sum(rainfall_period)

    max_rainfall = max(rainfall_period)

    average_rainfall = (
        total_rainfall / len(rainfall_period)
        if rainfall_period
        else 0
    )


    # ================= RISK =================

    current_risk, current_risk_score = calculate_combined_risk(

        latest_rainfall,

        latest_soil_moisture,

        last_6_hours_rainfall,

        last_12_hours_rainfall,

        last_3_days_rainfall,

        last_5_days_rainfall,

        last_12_days_rainfall,

        rainfall_trend

    )


    # ================= ALERT =================

    alert_message = generate_alert(
        current_risk,
        current_risk_score
    )


    if current_risk == "High":

        risk_message = (
            "High landslide risk. "
            "Immediate attention required."
        )

    elif current_risk == "Moderate":

        risk_message = (
            "Moderate landslide risk. "
            "Continue monitoring."
        )

    else:

        risk_message = (
            "Low landslide risk. "
            "Conditions are currently stable."
        )


    # ================= RESPONSE =================

    return {

        "location": {
            "latitude": latitude,
            "longitude": longitude
        },

        "latest_rainfall": latest_rainfall,

        "total_records": len(rainfall_period),

        "total_rainfall": total_rainfall,

        "average_rainfall": average_rainfall,

        "max_rainfall": max_rainfall,

        "last_6_hours_rainfall": last_6_hours_rainfall,

        "last_12_hours_rainfall": last_12_hours_rainfall,

        "last_3_days_rainfall": last_3_days_rainfall,

        "last_5_days_rainfall": last_5_days_rainfall,

        "last_12_days_rainfall": last_12_days_rainfall,

        "rainfall_trend": rainfall_trend,

        "latest_soil_moisture": latest_soil_moisture,

        "current_risk": current_risk,

        "current_risk_score": current_risk_score,

        "risk_message": risk_message,

        "alert_message": alert_message

    }
@app.get("/rainfall/chart")
def rainfall_chart(latitude: float, longitude: float):

    url = "https://api.open-meteo.com/v1/forecast"

    params = {
        "latitude": latitude,
        "longitude": longitude,
        "hourly": "precipitation",
        "past_days": 2,
        "forecast_days": 1,
        "timezone": "Asia/Kolkata"
    }

    response = requests.get(url, params=params)

    if response.status_code != 200:
        return {
            "error": "Unable to fetch rainfall data"
        }

    data = response.json()

    times = data["hourly"]["time"]
    rainfall = data["hourly"]["precipitation"]

    # Last 24 hours only
    times = times[-24:]
    rainfall = rainfall[-24:]

    return {
        "location": {
            "latitude": latitude,
            "longitude": longitude
        },
        "time": times,
        "rainfall": rainfall
    }

@app.get("/alerts")
def get_alerts(latitude: float, longitude: float):

    url = "https://api.open-meteo.com/v1/forecast"

    params = {
        "latitude": latitude,
        "longitude": longitude,
        "hourly": "precipitation,soil_moisture_0_to_1cm",
        "past_days": 12,
        "forecast_days": 1,
        "timezone": "Asia/Kolkata"
    }

    response = requests.get(url, params=params)

    if not response.ok:
        return {
            "alert": "Weather data could not be fetched.",
            "risk": "Unknown"
        }

    data = response.json()

    rainfall_values = data["hourly"]["precipitation"]
    soil_moisture_values = data["hourly"]["soil_moisture_0_to_1cm"]
    time_values = data["hourly"]["time"]

    # ================= CURRENT HOUR =================

    current_time = datetime.now().strftime("%Y-%m-%dT%H:00")

    try:
        current_index = time_values.index(current_time)
    except ValueError:
        return {
            "alert": "Current weather data is not available.",
            "risk": "Unknown"
        }

    latest_rainfall = rainfall_values[current_index] or 0
    latest_soil_moisture = soil_moisture_values[current_index] or 0

    # ================= 6 HOURS =================

    start_6 = max(0, current_index - 5)

    last_6_hours_rainfall = sum(
        value or 0
        for value in rainfall_values[start_6:current_index + 1]
    )

    # ================= PREVIOUS 6 HOURS =================

    previous_start = max(0, current_index - 11)
    previous_end = max(0, current_index - 5)

    previous_6_hours_rainfall = sum(
        value or 0
        for value in rainfall_values[previous_start:previous_end]
    )

    # ================= 12 HOURS =================

    start_12 = max(0, current_index - 11)

    last_12_hours_rainfall = sum(
        value or 0
        for value in rainfall_values[start_12:current_index + 1]
    )

    # ================= 3 DAYS =================

    start_3_days = max(0, current_index - 71)

    last_3_days_rainfall = sum(
        value or 0
        for value in rainfall_values[start_3_days:current_index + 1]
    )

    # ================= 5 DAYS =================

    start_5_days = max(0, current_index - 119)

    last_5_days_rainfall = sum(
        value or 0
        for value in rainfall_values[start_5_days:current_index + 1]
    )

    # ================= 12 DAYS =================

    start_12_days = max(0, current_index - 287)

    last_12_days_rainfall = sum(
        value or 0
        for value in rainfall_values[start_12_days:current_index + 1]
    )

    # ================= RAINFALL TREND =================

    if last_6_hours_rainfall > previous_6_hours_rainfall:
        rainfall_trend = "Increasing"

    elif last_6_hours_rainfall < previous_6_hours_rainfall:
        rainfall_trend = "Decreasing"

    else:
        rainfall_trend = "Stable"

    # ================= RISK =================

    risk, risk_score = calculate_combined_risk(
        rainfall=latest_rainfall,
        soil_moisture=latest_soil_moisture,
        last_6_hours_rainfall=last_6_hours_rainfall,
        last_12_hours_rainfall=last_12_hours_rainfall,
        last_3_days_rainfall=last_3_days_rainfall,
        last_5_days_rainfall=last_5_days_rainfall,
        last_12_days_rainfall=last_12_days_rainfall,
        rainfall_trend=rainfall_trend
    )

    # ================= ALERT =================

    alert = generate_alert(
        risk,
        risk_score
    )

    return {
        "location": {
            "latitude": latitude,
            "longitude": longitude
        },

        "latest_rainfall": latest_rainfall,

        "latest_soil_moisture": latest_soil_moisture,

        "last_6_hours_rainfall": last_6_hours_rainfall,

        "last_12_hours_rainfall": last_12_hours_rainfall,

        "rainfall_trend": rainfall_trend,

        "risk": risk,

        "risk_score": risk_score,

        "alert": alert
    }

@app.get("/risk-grid")
def risk_grid():

    # NER ke 8 representative monitoring points
    grid_points = [
        {
            "state": "Arunachal Pradesh",
            "latitude": 27.5860,
            "longitude": 91.8590
        },
        {
            "state": "Assam",
            "latitude": 26.7509,
            "longitude": 94.2037
        },
        {
            "state": "Manipur",
            "latitude": 24.8170,
            "longitude": 93.9368
        },
        {
            "state": "Meghalaya",
            "latitude": 25.2840,
            "longitude": 91.7210
        },
        {
            "state": "Mizoram",
            "latitude": 23.7271,
            "longitude": 92.7176
        },
        {
            "state": "Nagaland",
            "latitude": 25.6751,
            "longitude": 94.1086
        },
        {
            "state": "Sikkim",
            "latitude": 27.3389,
            "longitude": 88.6065
        },
        {
            "state": "Tripura",
            "latitude": 23.8315,
            "longitude": 91.2868
        }
    ]

    url = "https://api.open-meteo.com/v1/forecast"

    # 8 coordinates ek hi request mein
    latitudes = ",".join(
        str(point["latitude"])
        for point in grid_points
    )

    longitudes = ",".join(
        str(point["longitude"])
        for point in grid_points
    )

    params = {
        "latitude": latitudes,
        "longitude": longitudes,
        "hourly": "precipitation,soil_moisture_0_to_1cm",
        "past_days": 1,
        "forecast_days": 1,
        "timezone": "Asia/Kolkata"
    }

    try:

        response = requests.get(
            url,
            params=params,
            timeout=20
        )

        if response.status_code != 200:
            return {
                "error": "Unable to fetch Open-Meteo data",
                "status_code": response.status_code,
                "details": response.text
            }

        data = response.json()

        # Multiple locations ka response list hota hai
        if isinstance(data, dict):
            data = [data]

    except requests.RequestException as e:

        return {
            "error": "Open-Meteo connection failed",
            "details": str(e)
        }

    results = []

    for index, location_data in enumerate(data):

        point = grid_points[index]

        rainfall_values = location_data["hourly"]["precipitation"]
        soil_values = location_data["hourly"]["soil_moisture_0_to_1cm"]

        latest_rainfall = rainfall_values[-1]
        latest_soil = soil_values[-1]

        last_6_hours = sum(rainfall_values[-6:])
        last_12_hours = sum(rainfall_values[-12:])

        # Abhi 1 day hi available hai
        last_3_days = 0
        last_5_days = 0
        last_12_days = 0

        # Rainfall trend
        first_6 = sum(rainfall_values[-12:-6])
        second_6 = sum(rainfall_values[-6:])

        if second_6 > first_6 * 1.2:
            trend = "Increasing"

        elif second_6 < first_6 * 0.8:
            trend = "Decreasing"

        else:
            trend = "Stable"

        # Risk calculate
        risk, score = calculate_combined_risk(
            latest_rainfall,
            latest_soil,
            last_6_hours,
            last_12_hours,
            last_3_days,
            last_5_days,
            last_12_days,
            trend
        )

        results.append({
            "state": point["state"],
            "latitude": point["latitude"],
            "longitude": point["longitude"],
            "rainfall": latest_rainfall,
            "soil_moisture": latest_soil,
            "rainfall_trend": trend,
            "risk": risk,
            "score": score
        })

    return {
        "region": "North Eastern Region",
        "total_points": len(results),
        "grid": results
    }

@app.get("/high-risk-zones")
def high_risk_zones():

    locations = [
        {
            "name": "Tawang",
            "state": "Arunachal Pradesh",
            "latitude": 27.5860,
            "longitude": 91.8590
        },
        {
            "name": "Cherrapunji",
            "state": "Meghalaya",
            "latitude": 25.2840,
            "longitude": 91.7210
        },
        {
            "name": "Kohima",
            "state": "Nagaland",
            "latitude": 25.6751,
            "longitude": 94.1086
        },
        {
            "name": "Imphal",
            "state": "Manipur",
            "latitude": 24.8170,
            "longitude": 93.9368
        },
        {
            "name": "Aizawl",
            "state": "Mizoram",
            "latitude": 23.7271,
            "longitude": 92.7176
        },
        {
            "name": "Gangtok",
            "state": "Sikkim",
            "latitude": 27.3389,
            "longitude": 88.6065
        },
        {
            "name": "Agartala",
            "state": "Tripura",
            "latitude": 23.8315,
            "longitude": 91.2868
        },
        {
            "name": "Jorhat",
            "state": "Assam",
            "latitude": 26.7509,
            "longitude": 94.2037
        }
    ]

    results = []

    for location in locations:

        try:

            url = "https://api.open-meteo.com/v1/forecast"

            params = {
                "latitude": location["latitude"],
                "longitude": location["longitude"],
                "hourly": "precipitation,soil_moisture_0_to_1cm",
                "past_days": 1,
                "forecast_days": 1,
                "timezone": "Asia/Kolkata"
            }

            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()

            weather_data = response.json()

            rainfall = weather_data["hourly"]["precipitation"][-1] or 0
            soil_moisture = (
                weather_data["hourly"]["soil_moisture_0_to_1cm"][-1] or 0
            )

            risk, score = calculate_combined_risk(
                rainfall=rainfall,
                soil_moisture=soil_moisture,
                last_6_hours_rainfall=0,
                last_12_hours_rainfall=0,
                last_3_days_rainfall=0,
                last_5_days_rainfall=0,
                last_12_days_rainfall=0,
                rainfall_trend="Stable"
            )

            results.append({
                "name": location["name"],
                "state": location["state"],
                "latitude": location["latitude"],
                "longitude": location["longitude"],
                "rainfall": rainfall,
                "soil_moisture": soil_moisture,
                "risk_level": risk,
                "risk_score": score
            })

        except Exception as e:

            results.append({
                "name": location["name"],
                "state": location["state"],
                "latitude": location["latitude"],
                "longitude": location["longitude"],
                "rainfall": None,
                "soil_moisture": None,
                "risk_level": "Unknown",
                "risk_score": 0
            })

    results.sort(
        key=lambda x: x["risk_score"],
        reverse=True
    )

    return {
        "total_zones": len(results),
        "zones": results
    }


@app.get("/rainfall/forecast-risk")
def forecast_risk(latitude: float, longitude: float):

    url = "https://api.open-meteo.com/v1/forecast"

    params = {
        "latitude": latitude,
        "longitude": longitude,
        "hourly": "precipitation,soil_moisture_0_to_1cm",
        "forecast_days": 12,
        "timezone": "Asia/Kolkata"
    }

    response = requests.get(url, params=params)

    if not response.ok:
        return {
            "error": "Forecast data could not be fetched"
        }

    data = response.json()

    rainfall_values = data["hourly"]["precipitation"]
    soil_moisture_values = data["hourly"]["soil_moisture_0_to_1cm"]
    time_values = data["hourly"]["time"]

    forecast_risk = []
    forecast_scores = []

    for current_index, (time, rainfall, soil_moisture) in enumerate(
        zip(
            time_values,
            rainfall_values,
            soil_moisture_values
        )
    ):

        rainfall = rainfall or 0
        soil_moisture = soil_moisture or 0

        # ================= 6 HOURS =================

        start_6 = max(0, current_index - 5)

        last_6_hours_rainfall = sum(
            value or 0
            for value in rainfall_values[
                start_6:current_index + 1
            ]
        )

        # ================= PREVIOUS 6 HOURS =================

        previous_start = max(0, current_index - 11)
        previous_end = max(0, current_index - 5)

        previous_6_hours_rainfall = sum(
            value or 0
            for value in rainfall_values[
                previous_start:previous_end
            ]
        )

        # ================= 12 HOURS =================

        start_12 = max(0, current_index - 11)

        last_12_hours_rainfall = sum(
            value or 0
            for value in rainfall_values[
                start_12:current_index + 1
            ]
        )

        # ================= 3 DAYS =================

        start_3_days = max(0, current_index - 71)

        last_3_days_rainfall = sum(
            value or 0
            for value in rainfall_values[
                start_3_days:current_index + 1
            ]
        )

        # ================= 5 DAYS =================

        start_5_days = max(0, current_index - 119)

        last_5_days_rainfall = sum(
            value or 0
            for value in rainfall_values[
                start_5_days:current_index + 1
            ]
        )

        # ================= 12 DAYS =================

        start_12_days = max(0, current_index - 287)

        last_12_days_rainfall = sum(
            value or 0
            for value in rainfall_values[
                start_12_days:current_index + 1
            ]
        )

        # ================= RAINFALL TREND =================

        if last_6_hours_rainfall > previous_6_hours_rainfall:
            rainfall_trend = "Increasing"

        elif last_6_hours_rainfall < previous_6_hours_rainfall:
            rainfall_trend = "Decreasing"

        else:
            rainfall_trend = "Stable"

        # ================= RISK =================

        risk, score = calculate_combined_risk(
            rainfall=rainfall,
            soil_moisture=soil_moisture,
            last_6_hours_rainfall=last_6_hours_rainfall,
            last_12_hours_rainfall=last_12_hours_rainfall,
            last_3_days_rainfall=last_3_days_rainfall,
            last_5_days_rainfall=last_5_days_rainfall,
            last_12_days_rainfall=last_12_days_rainfall,
            rainfall_trend=rainfall_trend
        )

        forecast_risk.append(risk)
        forecast_scores.append(score)

    # ================= HIGHEST RISK =================

    highest_score = max(forecast_scores)

    highest_index = forecast_scores.index(
        highest_score
    )

    highest_risk = forecast_risk[highest_index]

    highest_risk_time = time_values[highest_index]

    # ================= RESPONSE =================

    return {
        "location": {
            "latitude": data["latitude"],
            "longitude": data["longitude"]
        },

        "timezone": data["timezone"],

        "forecast": {
            "time": time_values,
            "rainfall": rainfall_values,
            "soil_moisture": soil_moisture_values,
            "risk_level": forecast_risk,
            "risk_scores": forecast_scores
        },

        "highest_risk": {
            "risk_level": highest_risk,
            "risk_score": highest_score,
            "time": highest_risk_time
        }
    }
@app.post("/incident-reports")
def create_incident_report(
    name: str = Form(...),
    role: str = Form(...),
    state: str = Form(...),
    problem_type: str = Form(...),
    location: str = Form(...),
    description: str = Form(...),
    rating: str = Form(None),
    feedback: str = Form(None),
    files: list[UploadFile] | None = File(None)
):
    db = SessionLocal()

    saved_files = []

    try:
        # Save uploaded files
        if files:
            for file in files:

                if not file.filename:
                    continue

                safe_name = os.path.basename(file.filename)

                unique_name = (
                    f"{datetime.now().strftime('%Y%m%d%H%M%S%f')}_"
                    f"{safe_name}"
                )

                file_path = os.path.join("uploads", unique_name)

                with open(file_path, "wb") as buffer:
                    shutil.copyfileobj(file.file, buffer)

                saved_files.append(f"/uploads/{unique_name}")

        report = models.IncidentReport(
            name=name,
            role=role,
            state=state,
            problem_type=problem_type,
            location=location,
            description=description,
            photo=json.dumps(saved_files) if saved_files else None,
            rating=rating,
            feedback=feedback,
            status="Open",
            created_at=datetime.now()
        )

        db.add(report)
        db.commit()
        db.refresh(report)

        return {
            "message": "Incident report submitted successfully",
            "report_id": report.id,
            "status": report.status,
            "files": saved_files
        }

    finally:
        db.close()

@app.get("/incident-reports")
def get_incident_reports():

    db = SessionLocal()

    try:
        reports = (
            db.query(models.IncidentReport)
            .order_by(models.IncidentReport.id.desc())
            .all()
        )

        return [
            {
                "report_id": report.id,
                "name": report.name,
                "role": report.role,
                "state": report.state,
                "problem_type": report.problem_type,
                "location": report.location,
                "description": report.description,
                "photo": report.photo,
                "rating": report.rating,
                "feedback": report.feedback,
                "status": report.status,
                "created_at": report.created_at
            }
            for report in reports
        ]

    finally:
        db.close()

@app.put("/incident-reports/{report_id}/status")
def update_incident_report_status(
    report_id: int,
    status: str
):
    db = SessionLocal()

    try:
        report = (
            db.query(models.IncidentReport)
            .filter(models.IncidentReport.id == report_id)
            .first()
        )

        if not report:
            return {
                "error": "Report not found"
            }

        allowed_statuses = [
            "Open",
            "Under Review",
            "Resolved"
        ]

        if status not in allowed_statuses:
            return {
                "error": "Invalid status",
                "allowed_statuses": allowed_statuses
            }

        report.status = status

        db.commit()
        db.refresh(report)

        return {
            "message": "Report status updated successfully",
            "report_id": report.id,
            "status": report.status
        }

    finally:
        db.close()