# import requests library to make requests and work with API
import requests
# import pytz to get SGT
import pytz
import datetime

# the "region" parameter should be of type string and contain one of the following 6 values:
# "west", "national", "east", "central", "south", "north"

def getpsi(region):
    # set timezone to SG
    timezone = pytz.timezone('Asia/Singapore')

    # get datetime and localize it to SGT
    dt = datetime.datetime.now()
    now = timezone.localize(dt)

    # transform datetime into a format suitable for the PSI API
    param = now.strftime("%Y-%m-%d %H:%M:%S").replace(" ", "T")

    # making a GET request to the API endpoint, obtain output in a dictionary format with .json()
    response = requests.get("https://api.data.gov.sg/v1/environment/psi", param).json()
    psi = response["items"][0]["readings"]["psi_twenty_four_hourly"][region]

    # print(type(response.items))
    return psi

# for testing reasons:
# def main():
##     region = input("Region: ")
#     psi = getpsi(region)
#     print(psi)

# main()