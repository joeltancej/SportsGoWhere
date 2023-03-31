# import requests library to make requests and work with API
import requests
# import pytz to get SGT
import pytz
import datetime
# for dataframe
import pandas as pd
# for the math
from math import radians, cos, sin, asin, sqrt

def getcarparkdata():
    # making a GET request to the API endpoint, obtain output in a dictionary format with .json()
    response = requests.get("https://api.data.gov.sg/v1/transport/carpark-availability", get_dt()).json()
    try:
        data = response["items"][0]["carpark_data"]
    except:
        data = None
    return data

def getcarparkinfo(cpno):
    carparkdata = getcarparkdata()
    if carparkdata == None:
        return "Updating, refresh to load."
    # iterate through each dictionary of carpark information
    for info in carparkdata:
        # if the carpark number matches, return the availability
        if info["carpark_number"] == cpno:
            lots_available = info["carpark_info"][0]["lots_available"]
            total_lots = info["carpark_info"][0]["total_lots"]
            toreturn = "{}/{}".format(lots_available, total_lots)
            return toreturn
    return "Availability Data Unavailable."

# the "region" parameter should be of type string and contain one of the following 6 values:
# "west", "national", "east", "central", "south", "north"

def getpsi(lat, long):
    places = []
    lats = []
    longs = []
    # making a GET request to the API endpoint, obtain output in a dictionary format with .json()
    response = requests.get("https://api.data.gov.sg/v1/environment/psi", get_dt()).json()
    for place in response["region_metadata"]:
        places.append(place["name"])
        lats.append(float(place["label_location"]["latitude"]))
        longs.append(float(place["label_location"]["longitude"]))
    d = {'areas': places, 'lat': lats, 'lon': longs}
    df = pd.DataFrame(data=d)
    distances = df.apply(
        lambda row: dist(float(lat), float(long), row['lat'], row['lon']), 
        axis=1)
    index = distances.idxmin()
    area = response["region_metadata"][index]["name"]
    psi = response["items"][0]["readings"]["psi_twenty_four_hourly"][area]

    descriptor = ""
    advisory = ""
    if psi <= 50:
        descriptor = "Good"
        advisory = "Carry on with normal activities."
    elif psi > 50 and psi <=100:
        descriptor = "Moderate"
        advisory = "Carry on with normal activities."
    elif psi > 100 and psi <= 200:
        descriptor = "Unhealthy"
        advisory = "REDUCE prolonged or strenous outdoor physical exertion."
    elif psi > 200 and psi <= 300:
        descriptor = "Very Unhealthy"
        advisory = "AVOID prolonged or strenous outdoor physical exertion."
    else:
        descriptor = "Hazardous"
        advisory = "MINIMISE outdoor activity."

    # print(type(response.items))
    return psi, descriptor, advisory, area.capitalize()

def getfullpsi():
    # making a GET request to the API endpoint, obtain output in a dictionary format with .json()
    response = requests.get("https://api.data.gov.sg/v1/environment/psi", get_dt()).json()
    psi = response["items"][0]["readings"]["psi_twenty_four_hourly"]
    regions = psi.keys()
    readings = []
    for value in psi.values():
        readings.append(value)

    return regions, readings

def get4dayweather():
    # list to keep weather in 6-hour intervals (4 entries)
    weather = []
    dates = []
    temp = []
    # making a GET request to the API endpoint, obtain output in a dictionary format with .json()
    response = requests.get("https://api.data.gov.sg/v1/environment/4-day-weather-forecast", get_dt()).json()
    for forecast in response["items"][0]["forecasts"]:
        dates.append(forecast["date"])
        weather.append(forecast["forecast"])
        temp.append(str(forecast["temperature"]["low"]) + ' - ' + str(forecast["temperature"]["high"]))

    return weather, dates, temp

def get24hweather():
    # list to keep weather in 6-hour intervals (4 entries)
    weather = []
    # making a GET request to the API endpoint, obtain output in a dictionary format with .json()
    response = requests.get("https://api.data.gov.sg/v1/environment/24-hour-weather-forecast", get_dt()).json()
    for forecast in response["items"][0]["periods"]:
        weather.append(forecast["regions"])

    return weather

def getcurweather(lat, long):
    # list to keep weather in 6-hour intervals (4 entries)
    places = []
    lats = []
    longs = []
    # making a GET request to the API endpoint, obtain output in a dictionary format with .json()
    response = requests.get("https://api.data.gov.sg/v1/environment/2-hour-weather-forecast", get_dt()).json()
    for place in response["area_metadata"]:
        places.append(place["name"])
        lats.append(float(place["label_location"]["latitude"]))
        longs.append(float(place["label_location"]["longitude"]))
    d = {'places': places, 'lat': lats, 'lon': longs}
    df = pd.DataFrame(data=d)
    distances = df.apply(
        lambda row: dist(float(lat), float(long), row['lat'], row['lon']), 
        axis=1)
    index = distances.idxmin()
    region = response["area_metadata"][index]["name"]
    for forecast in response["items"][0]["forecasts"]:
        if forecast["area"] == region:
            return region, forecast["forecast"]
    return "Error"

def get_dt():
    # set timezone to SG
    timezone = pytz.timezone('Asia/Singapore')

    # get datetime and localize it to SGT
    dt = datetime.datetime.now()
    now = timezone.localize(dt)

    # transform datetime into a format suitable for the PSI API
    param = now.strftime("%Y-%m-%d %H:%M:%S").replace(" ", "T")

    return param

# Harversine equation - helps to find out closest carparks
def dist(lat1, long1, lat2, long2):
    """
    Calculate the great circle distance between two points 
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians 
    lat1, long1, lat2, long2 = map(radians, [lat1, long1, lat2, long2])
    # haversine formula 
    dlon = long2 - long1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    # Radius of earth in kilometers is 6371
    km = 6371* c
    return km