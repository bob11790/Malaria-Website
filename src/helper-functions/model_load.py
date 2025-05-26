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
    "latitude", 
    "longitude",
    "country",
    "month_start",
    "year_start",
    "month_end", # same as start
    "year_end", # same as start
    "month high",
    "month low",
    "month mean",
    "temp range",
    "total rain",
    "most rain",
    "most wind",
    "continentId",
    "mean_cases",
]

