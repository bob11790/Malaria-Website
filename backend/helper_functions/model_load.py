import ydf
import pandas as pd
import pycountry_convert as pc
import ydf.model
import math
import numpy as np
from helper_functions import helper_functions as hf

def continent_code(continent: str) -> str:
    if continent in CONT_MAP:
        return CONT_MAP[continent]
    else:
        return "-1"
    
CONT_MAP = {
        "Americas": 0,
        "Oceania": 1,
        "Asia":    2,
        "Africa":  3,
    }

INPUT_FORMAT = [
    "latitude", # float
    "longitude", # float
    "country",# country code() -> tuple[0] -> str
    "month_start", # int (single number)
    "year_start",# int (single number)
    "month_end", # same as start
    "year_end", # same as start
    "month high", #create_weather_data -> summary['month high']
    "month low", #create_weather_data -> summary['month low']
    "month mean", #create_weather_data -> summary['month mean']
    "temp range", #create_weather_data -> summary['temp range']
    "total rain", #create_weather_data -> summary['total rain']
    "most rain", #create_weather_data -> summary['most rain']
    "most wind", #create_weather_data -> summary['most wind']
    "continentId",# continent_code() -> str 
    "mean_cases",# country code() -> tuple[1]
]

"""
Dummy data
"""
LOCATION = (37.8136, 144.9631) # melbourne
LAT = LOCATION[0]
LON = LOCATION[1]
DAY = 27
MONTH = 5
YEAR = 2025
WEATHER = hf.create_weather_data(LAT,LON,DAY,MONTH,YEAR)
COUNTRY_INFO = hf.country_code("AUS")
COUNTRY = COUNTRY_INFO[0]
COUNTRY_MEAN = COUNTRY_INFO[1]

INPUT_VAL = [
    LAT,
    LON,
    COUNTRY,
    MONTH,
    YEAR,
    MONTH,
    YEAR,
    WEATHER["month high"],
    WEATHER["month low"],
    WEATHER["month mean"],
    WEATHER["temp range"],
    WEATHER["total rain"],
    WEATHER["most rain"],
    WEATHER["month high"],
    continent_code("Oceania"),
    COUNTRY_MEAN
    ]

MODEL = ydf.load_model("ydf_malaria_weather_model")

def predict(lat: float, lon: float, countryA3: str, continent: str, day: int, month: int, year: int, _debug:bool = False) -> float:
    WEATHER = hf.create_weather_data(lat, lon, day, month, year)
    COUNTRY, COUNTRY_MEAN = hf.country_code(countryA3)
    CONTINENT = continent_code(continent)
    # Build dictionary using INPUT_FORMAT keys
    input_data = {
        "latitude": lat,
        "longitude": lon,
        "country": COUNTRY,
        "month_start": month,
        "year_start": year,
        "month_end": month,
        "year_end": year,
        "month high": WEATHER.get("month high"),
        "month low": WEATHER.get("month low"),
        "month mean": WEATHER.get("month mean"),
        "temp range": WEATHER.get("temp range"),
        "total rain": WEATHER.get("total rain"),
        "most rain": WEATHER.get("most rain"),
        "most wind": WEATHER.get("most wind"),
        "continentId": CONTINENT,
        "mean_cases": COUNTRY_MEAN
    }
    

    _in = pd.DataFrame([input_data], columns=INPUT_FORMAT)
    prediction = MODEL.predict(_in)[0]
    if _debug == True:
        print(input_data)
    return {
    "prediction": float(prediction),
    "country": pc.country_alpha2_to_country_name(pc.country_alpha3_to_country_alpha2(countryA3)),
    "date": {
        "day": day,
        "month": month,
        "year": year
    },
    "weather_summary": WEATHER
    }





## debug path:
# import os
# print("cwd:", os.getcwd())

#Debug:
# INPUT = pd.DataFrame([INPUT_VAL], columns=INPUT_FORMAT)
# print(INPUT.head())
# print(MODEL.predict(INPUT)[0])


"""
Depricated function
"""

# just put in an list based on the INPUT_FORMAT
# the function will convert it to a dataframe
# and output the pr.

# def predict(input: list) -> float:
#     if len(input) != len(INPUT_FORMAT):
#         error.log("bad list at predict(input)")
#         return None
#     df = pd.DataFrame([input], columns=INPUT_FORMAT)
#     return float(MODEL.predict(df)[0])
