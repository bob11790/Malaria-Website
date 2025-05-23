import httpx
import pycountry
from fastapi import FastAPI
from pydantic import BaseModel, field_validator
from fastapi.middleware.cors import CORSMiddleware
from dateutil import parser
from collections import defaultdict
from datetime import datetime, timedelta



app = FastAPI()

origins = [
    "http://localhost:5173",
    "http://127.0.0.1:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, OPTIONS, etc)
    allow_headers=["*"],  # Allow all headers
)

class Coordinates(BaseModel):
    lat: float
    lng: float
    country: str

    # Validates some country name
    @field_validator("country", mode="before")
    @classmethod
    def normalize_country(cls, value):
        corrections = {
            "Congo-Brazzaville": "Republic of the Congo",
            "Democratic Republic of the Congo": "Congo, The Democratic Republic of the",
        }
        return corrections.get(value, value)

def country_name_to_code(name):
    try:
        country = pycountry.countries.search_fuzzy(name)[0]
        return country.alpha_3
    except:
        return None



@app.post("/coordinates")
async def receive_coordinates(coords: Coordinates):
    now = datetime.utcnow()
    today = now.date()
    week_ahead = today + timedelta(days=6)  # predictive range

    weather_url = (
        f"https://api.open-meteo.com/v1/forecast?"
        f"latitude={coords.lat}&longitude={coords.lng}"
        f"&current_weather=true"
        f"&hourly=temperature_2m,precipitation,windspeed_10m"
        f"&daily=precipitation_sum"
        f"&timezone=auto"
    )

    async with httpx.AsyncClient() as client:
        response = await client.get(weather_url)
        response.raise_for_status()
        weather_data = response.json()

    # Extract hourly data
    hourly = weather_data.get("hourly", {})
    hourly_times = [parser.isoparse(t) for t in hourly.get("time", [])]
    today_temps = [hourly["temperature_2m"][i] for i, dt in enumerate(hourly_times) if dt.date() == today]
    today_wind = [hourly["windspeed_10m"][i] for i, dt in enumerate(hourly_times) if dt.date() == today]

    # Compute today's temperature stats
    if today_temps:
        day_high = max(today_temps)
        day_low = min(today_temps)
        day_mean = sum(today_temps) / len(today_temps)
        temp_range = day_high - day_low
    else:
        day_high = day_low = day_mean = temp_range = None

    # Compute average wind speed for today
    day_wind_speed = sum(today_wind) / len(today_wind) if today_wind else None

    # Extract 7-day precipitation forecast
    daily = weather_data.get("daily", {})
    daily_dates = [parser.isoparse(d).date() for d in daily.get("time", [])]
    daily_precip = dict(zip(daily_dates, daily.get("precipitation_sum", [])))

    future_7_days = {date: mm for date, mm in daily_precip.items() if today <= date <= week_ahead}
    todays_rain = future_7_days.get(today, 0)
    total_rain = sum(future_7_days.values())
    most_rain = max(future_7_days.values()) if future_7_days else 0


    # Print outputs
    print(f"start_month: {now.month}, end_month: {now.month}, start_year: {now.year}, end_year: {now.year}")
    print(f"day_high: {day_high}, day_low: {day_low}, day_mean: {day_mean}, temp_range: {temp_range}")
    print(f"todays_rain: {todays_rain}, most_rain: {most_rain}, total_rain: {total_rain}, day_wind_speed: {day_wind_speed}")

    return {
        "start_month": now.month,
        "end_month": now.month,
        "start_year": now.year,
        "end_year": now.year,
        "day_high": day_high,
        "day_low": day_low,
        "day_mean": day_mean,
        "temp_range": temp_range,
        "todays_rain": todays_rain,
        "total_rain": total_rain,
        "most_rain": most_rain,
        "day_wind_speed": day_wind_speed,
    }