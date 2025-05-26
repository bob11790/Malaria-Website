import ydf
import pandas as pd

# just put in an list based on the INPUT_FORMAT
# the function will convert it to a dataframe
# and output the pr.
def predict(input: list) -> float:
    if len(input) != len(INPUT_FORMAT):
        error.log("bad list at predict(input)")
        return None
    df = pd.DataFrame([input], columns=INPUT_FORMAT)
    return float(MODEL.predict(df)[0])

MODEL = ydf.Model.load("../../ydf_malaria_weather_model/ydf_malaria_weather_model/")

INPUT_FORMAT = [
    "Unnamed: 0", # -1
    "site_id",# -1
    "latitude", # float
    "longitude", # float
    "country",# country code() -> tuple[0]
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
    "continentId",# continent_code() -> int
    "mean_cases",# country code() -> tuple[1]
]

