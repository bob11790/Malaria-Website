import httpx
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
from dateutil import parser

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


@app.post("/coordinates")
async def receive_coordinates(coords: Coordinates):
    print(f"Received coordinates: lat={coords.lat}, lng={coords.lng}, country={coords.country}")

    weather_url = (
        f"https://api.open-meteo.com/v1/forecast?"
        f"latitude={coords.lat}&longitude={coords.lng}&current_weather=true"
        f"&hourly=relativehumidity_2m,precipitation"
    )

    async with httpx.AsyncClient() as client:
        response = await client.get(weather_url)
        response.raise_for_status()
        weather_data = response.json()

    current_weather = weather_data.get("current_weather", {})
    hourly = weather_data.get("hourly", {})
    times = hourly.get("time", [])

    humidity_list = hourly.get("relativehumidity_2m", [])
    precipitation_list = hourly.get("precipitation", [])

    current_time_str = current_weather.get("time")

    humidity = None
    precipitation = None

    if current_time_str and times:
        current_time = parser.isoparse(current_time_str)

        # Parse all hourly times to datetime objects
        hourly_times = [parser.isoparse(t) for t in times]

        # Find the closest hourly time index to current_time
        closest_idx = min(range(len(hourly_times)), key=lambda i: abs(hourly_times[i] - current_time))

        humidity = humidity_list[closest_idx] if closest_idx < len(humidity_list) else None
        precipitation = precipitation_list[closest_idx] if closest_idx < len(precipitation_list) else None

    print(f"Current weather: {current_weather}")
    print(f"Humidity at closest hourly time: {humidity}")
    print(f"Precipitation at closest hourly time: {precipitation}")

    return {
        "message": "Coordinates and weather received",
        "lat": coords.lat,
        "lng": coords.lng,
        "country": coords.country,
        "current_weather": current_weather,
        "humidity": humidity,
        "precipitation": precipitation,
    }