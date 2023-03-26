# import requests library to make requests and work with API
import requests
# import pytz to get SGT
import pytz
import datetime

def getcarparkdata():
    # making a GET request to the API endpoint, obtain output in a dictionary format with .json()
    response = requests.get("https://api.data.gov.sg/v1/transport/carpark-availability", get_dt()).json()
    return response["items"][0]["carpark_data"]

def getcarparkinfo(cpno):
    carparkdata = getcarparkdata()
    # iterate through each dictionary of carpark information
    for info in carparkdata:
        # if the carpark number matches, return the availability
        if info["carpark_number"] == cpno:
            lots_available = info["carpark_info"][0]["lots_available"]
            total_lots = info["carpark_info"][0]["total_lots"]
            toreturn = "{}/{}".format(lots_available, total_lots)
            return toreturn
    return "Error: Carpark Not Found"

# the "region" parameter should be of type string and contain one of the following 6 values:
# "west", "national", "east", "central", "south", "north"

def getpsi(region):
    # making a GET request to the API endpoint, obtain output in a dictionary format with .json()
    response = requests.get("https://api.data.gov.sg/v1/environment/psi", get_dt()).json()
    psi = response["items"][0]["readings"]["psi_twenty_four_hourly"][region]

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
    return psi, descriptor, advisory

def gettemp():
    # making a GET request to the API endpoint, obtain output in a dictionary format with .json()
    response = requests.get("https://api.data.gov.sg/v1/environment/air-temperature", get_dt()).json()
    temperature = response["items"][0]["readings"][0]["value"]

    # print(type(response.items))
    return temperature

def getrain():
    # making a GET request to the API endpoint, obtain output in a dictionary format with .json()
    response = requests.get("https://api.data.gov.sg/v1/environment/rainfall", get_dt()).json()
    rainfall = response["items"][0]["readings"][0]["value"]

    # print(type(response.items))
    return rainfall

def get_dt():
    # set timezone to SG
    timezone = pytz.timezone('Asia/Singapore')

    # get datetime and localize it to SGT
    dt = datetime.datetime.now()
    now = timezone.localize(dt)

    # transform datetime into a format suitable for the PSI API
    param = now.strftime("%Y-%m-%d %H:%M:%S").replace(" ", "T")

    return param