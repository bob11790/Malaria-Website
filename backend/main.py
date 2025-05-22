from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

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

@app.post("/coordinates")
async def receive_coordinates(coords: Coordinates):
    print(f"Received coordinates: lat={coords.lat}, lng={coords.lng}")
    # You can store or process coordinates here
    return {"message": "Coordinates received", "lat": coords.lat, "lng": coords.lng}