############################################################################
# Imports
############################################################################

import openmeteo_requests
import requests_cache
import pandas as pd
import geocoder

from astral.sun import sun
from astral import LocationInfo
from datetime import datetime
from retry_requests import retry

############################################################################
# Variables
############################################################################

API_URL = "https://api.open-meteo.com/v1/forecast"
DABO_LATITUDE = 48.65
DABO_LONGITUDE = 7.23

MAXIMUM_CLOUD_COVERAGE = 60 # Cloud coverage percentage
MINIMUM_CLEAR_TIME = 4 # Hours of consecutive clear sky

############################################################################
# Private Methods
############################################################################


############################################################################
# Public Methods
############################################################################

def _get__cloud_params():

    params = {

        "latitude": DABO_LATITUDE,
        "longitude": DABO_LONGITUDE,
        "hourly": ["cloud_cover", "cloud_cover_low", "cloud_cover_mid", "cloud_cover_high"],
        "timezone": "Europe/Berlin",
        "forecast_days": 3

    }

    return params

def _weather_api_request(params):

    cache_session = requests_cache.CachedSession('.cache', expire_after = 3600)
    retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
    openmeteo = openmeteo_requests.Client(session = retry_session)

    responses = openmeteo.weather_api(API_URL, params=params)    

    return responses[0]

def _process_api_response(api_response):

    hourly = api_response.Hourly()
    hourly_cloud_cover = hourly.Variables(0).ValuesAsNumpy()
    hourly_cloud_cover_low = hourly.Variables(1).ValuesAsNumpy()
    hourly_cloud_cover_mid = hourly.Variables(2).ValuesAsNumpy()
    hourly_cloud_cover_high = hourly.Variables(3).ValuesAsNumpy()

    hourly_data = {"date": pd.date_range(
        start = pd.to_datetime(hourly.Time(), unit = "s", utc = True),
        end = pd.to_datetime(hourly.TimeEnd(), unit = "s", utc = True),
        freq = pd.Timedelta(seconds = hourly.Interval()),
        inclusive = "left"
    )}
    hourly_data["cloud_cover"] = hourly_cloud_cover
    hourly_data["cloud_cover_low"] = hourly_cloud_cover_low
    hourly_data["cloud_cover_mid"] = hourly_cloud_cover_mid
    hourly_data["cloud_cover_high"] = hourly_cloud_cover_high

    cloud_coverage_report = pd.DataFrame(data = hourly_data)

    return cloud_coverage_report

def _get_clear_sky_windows(cloud_coverage_report):

    Cloud_Coverage_Array = cloud_coverage_report['cloud_cover']

    First_Clear_Hour = 0
    Last_clear_Hour = 0
    Clear_Windows = []
    Clear_Date_Windows = []

    for Cloud_Coverage_Index in range(len(Cloud_Coverage_Array)-1):

        if Cloud_Coverage_Array[Cloud_Coverage_Index+1] <= MAXIMUM_CLOUD_COVERAGE and Cloud_Coverage_Array[Cloud_Coverage_Index] <= MAXIMUM_CLOUD_COVERAGE:

            Last_clear_Hour = Cloud_Coverage_Index + 1

        elif Cloud_Coverage_Array[Cloud_Coverage_Index+1] <= MAXIMUM_CLOUD_COVERAGE and Cloud_Coverage_Array[Cloud_Coverage_Index] > MAXIMUM_CLOUD_COVERAGE:

            First_Clear_Hour = Cloud_Coverage_Index + 1

        elif Cloud_Coverage_Array[Cloud_Coverage_Index+1] > MAXIMUM_CLOUD_COVERAGE and Cloud_Coverage_Array[Cloud_Coverage_Index] <= MAXIMUM_CLOUD_COVERAGE:

            if Last_clear_Hour-First_Clear_Hour >= MINIMUM_CLEAR_TIME:

                Clear_Windows.append((First_Clear_Hour, Last_clear_Hour))

    for Clear_Window in Clear_Windows:

        Date_Array = cloud_coverage_report['date']

        Clear_Date_Windows.append((Date_Array[Clear_Window[0]], Date_Array[Clear_Window[1]]))

    return Clear_Date_Windows

def _get_sun_information():
    
    print("")




############################################################################
# Main
############################################################################

def Get_Clear_Sky_Report():

    cloud_coverage = _weather_api_request(_get__cloud_params())
    cloud_coverage_report = _process_api_response(cloud_coverage)

    Clear_Sky_Flag = False
    Clear_Sky_Date = ""
    Clear_Sky_Start = ""
    Clear_Sky_Stop = ""

    Clear_Date_Windows = _get_clear_sky_windows(cloud_coverage_report)
    print(Clear_Date_Windows)

    _get_sun_information()

    return Clear_Sky_Flag, Clear_Sky_Date, Clear_Sky_Start, Clear_Sky_Stop

# Get_Clear_Sky_Report()