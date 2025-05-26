import ydf
import pandas as pd
import ydf.model
from helper_functions import continent_code, country_code, create_weather_data 

INPUT_FORMAT = [
    "latitude", # float
    "LONitude", # float
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
WEATHER = create_weather_data(LAT,LON,DAY,MONTH,YEAR)
COUNTRY_INFO = country_code("Australia")
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
    continent_code("Oceana"),
    COUNTRY_MEAN
    ]

MODEL = ydf.load_model("backend/ydf_malaria_weather_model")

def predict(lat:float, lon:float,country:str,continent:str, day:int ,month:int ,year:int ) -> float:
    LOCATION = (37.8136, 144.9631)
    LAT = lat
    LON = lon
    DAY = day
    MONTH = month
    YEAR = year
    WEATHER = create_weather_data(LAT,LON,DAY,MONTH,YEAR)
    COUNTRY_INFO = country_code(country)
    COUNTRY = COUNTRY_INFO[0]
    COUNTRY_MEAN = COUNTRY_INFO[1]
    _in = pd.DataFrame([INPUT_VAL], columns=INPUT_FORMAT)
    return MODEL.predict(_in)[0]


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
