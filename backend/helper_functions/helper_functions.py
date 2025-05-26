from meteostat import Point, Daily, Stations
from datetime import datetime, timedelta
import pycountry_convert as pc
import calendar
import pandas as pd


def continent_code(country: str) -> int:
    continent = alpha3_to_continent(country)
    if continent in CONT_MAP:
        return CONT_MAP[continent]
    else:
        return -1

def country_code(country: str) -> tuple:
    if country in PYCOUNTRY_MAP:
        id_mean = (PYCOUNTRY_MAP[country]["id"], PYCOUNTRY_MAP[country]["mean"])
        return id_mean
    else:
        return (-1, 0)

def create_weather_data(lat: float, lon: float, day: int, month: int, year: int) -> dict:

    #7 day weather summary
    summary = {col: 0 for col in WEATHER_COLS} # safely creates keys with 0 intialised
    station = Stations()
    location = station.nearby(lat,lon).fetch(1)
    start_day = datetime(year, month, day) - timedelta(days=7) # gets the last week
    end_day   = datetime(year, month, day)
  
    #meteo stat
    weather = Daily(location, start_day, end_day).fetch()

    # creates the mean for each metric
    if 'tmax' in weather.columns:
        summary['month high'] = weather['tmax'].max()
    if 'tmin' in weather.columns:
        summary['month low'] = weather['tmin'].min()
    if 'tavg' in weather.columns:
        summary['month mean'] = weather['tavg'].mean() #just called month mean, itsll be more like 72 hour mean
    if {'tmax','tmin'}.issubset(weather.columns):
        summary['temp range'] = weather['tmax'].max() - weather['tmin'].min()
    if 'prcp' in weather.columns:
        summary['total rain'] = weather['prcp'].sum()
        summary['most rain']  = weather['prcp'].max()
    if 'wspd' in weather.columns:
        summary['most wind']  = weather['wspd'].max()

    return summary # plug this right into the input for the model

def alpha3_to_continent(alpha3):
    try:
        # Get the 2-letter country code from alpha3
        country_alpha2 = pc.country_alpha3_to_country_alpha2(alpha3)
        # Get continent code (e.g., 'NA', 'SA', 'AS', 'AF', 'OC', 'EU')
        continent_code = pc.country_alpha2_to_continent_code(country_alpha2)
        
        # Map continent_code to your CONT_MAP keys
        if continent_code in ['NA', 'SA']:
            return CONT_MAP["Americas"]
        elif continent_code == 'OC':
            return CONT_MAP["Oceania"]
        elif continent_code == 'AS':
            return CONT_MAP["Asia"]
        elif continent_code == 'AF':
            return CONT_MAP["Africa"]
        else:
            # Europe (EU) or Antarctica (AN) or unknown
            return None
    except Exception as e:
        # Handle missing/invalid alpha3 codes here
        print(f"Warning: Could not map {alpha3} to continent: {e}")
        return None

WEATHER_COLS = [
    'month high',
    'month low',
    'month mean',
    'temp range',
    'total rain',
    'most rain',
    'most wind'
]

CONT_MAP = {
        "Americas": 0,
        "Oceania": 1,
        "Asia":    2,
        "Africa":  3,
    }

# Mapping from ISO Alpha-3, retrieves id and mean for last 10 years per thousand malaria infections
PYCOUNTRY_MAP = {
    "VEN": {"id":  0, "mean":   298724},
    "COL": {"id":  1, "mean":    76646},
    "PER": {"id":  2, "mean":    37016},
    "BRA": {"id":  3, "mean":   183284},
    "SLB": {"id":  4, "mean":    96693},
    "THA": {"id":  5, "mean":    11428},
    "VUT": {"id":  6, "mean":     1117},
    "PNG": {"id":  7, "mean":   856356},
    "VNM": {"id":  8, "mean":     6008},
    "TLS": {"id":  9, "mean":       27},
    "PAK": {"id": 10, "mean":  1660333},
    "LKA": {"id": 11, "mean":       44},
    "LAO": {"id": 12, "mean":     9579},
    "MMR": {"id": 13, "mean":   114944},
    "MYS": {"id": 14, "mean":    3362},
    "IND": {"id": 15, "mean":   513544},
    "IDN": {"id": 16, "mean":   287867},
    "KHM": {"id": 17, "mean":    33650},
    "BGD": {"id": 18, "mean":    19187},
    "AFG": {"id": 19, "mean":   245071},
    "ZWE": {"id": 20, "mean":   353460},
    "ZMB": {"id": 21, "mean":  6703057},
    "UGA": {"id": 22, "mean": 14738576},
    "TGO": {"id": 23, "mean":  1966231},
    "TZA": {"id": 24, "mean":  5841353},
    "SDN": {"id": 25, "mean":  3112750},
    "SSD": {"id": 26, "mean":  3638410},
    "ZAF": {"id": 27, "mean":    10522},
    "SOM": {"id": 28, "mean":    38430},
    "SLE": {"id": 29, "mean":  1851427},
    "SEN": {"id": 30, "mean":   419736},
    "RWA": {"id": 31, "mean":  2698357},
    "NER": {"id": 32, "mean": 13386947},
    "MOZ": {"id": 33, "mean": 10874010},
    "NGA": {"id": 34, "mean": 22367338},
    "MRT": {"id": 35, "mean":   143792},
    "MWI": {"id": 36, "mean":  5744232},
    "MLI": {"id": 37, "mean":  3237176},
    "MDG": {"id": 38, "mean":  1632030},
    "LBR": {"id": 39, "mean":  1332205},
    "GNB": {"id": 40, "mean":   156990},
    "GIN": {"id": 41, "mean":   800593},
    "KEN": {"id": 42, "mean":  7278835},
    "GAB": {"id": 43, "mean":   220385},
    "GMB": {"id": 44, "mean":   114741},
    "GHA": {"id": 45, "mean":  8641515},
    "ERI": {"id": 46, "mean":    66596},
    "GNQ": {"id": 47, "mean":    58381},
    "ETH": {"id": 48, "mean":  1841944},
    "CIV": {"id": 49, "mean":  5946777},
    "TCD": {"id": 50, "mean":  1778788},
    "COM": {"id": 51, "mean":    11329},
    "CAF": {"id": 52, "mean":  1800579},
    "CMR": {"id": 53, "mean":  3106740},
    "BDI": {"id": 54, "mean":  7100293},
    "BFA": {"id": 55, "mean": 10650641},
    "AGO": {"id": 56, "mean":  6898331},
    "BEN": {"id": 57, "mean":  2366973},
}
