# import requests library to make requests and work with API
import requests
# import from sgdatetime to get the SGT parameters
import sgdatetime

# the "region" parameter should be of type string and contain one of the following 6 values:
# "west", "national", "east", "central", "south", "north"

def getpsi(region):
    # making a GET request to the API endpoint, obtain output in a dictionary format with .json()
    response = requests.get("https://api.data.gov.sg/v1/environment/psi", sgdatetime.get_dt()).json()
    psi = response["items"][0]["readings"]["psi_twenty_four_hourly"][region]

    # print(type(response.items))
    return psi

# for testing reasons:
# def main():
    ## region = input("Region: ")
#     psi = getpsi(region)
#     print(psi)

# main()