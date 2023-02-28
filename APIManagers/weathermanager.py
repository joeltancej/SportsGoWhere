# import requests library to make requests and work with API
import requests
# import from sgdatetime to get the SGT parameters
import sgdatetime

# for comments

def gettemp():
    # making a GET request to the API endpoint, obtain output in a dictionary format with .json()
    response = requests.get("https://api.data.gov.sg/v1/environment/air-temperature", sgdatetime.get_dt()).json()
    temperature = response["items"][0]["readings"][0]["value"]

    # print(type(response.items))
    return temperature

def getrain():
    # making a GET request to the API endpoint, obtain output in a dictionary format with .json()
    response = requests.get("https://api.data.gov.sg/v1/environment/rainfall", sgdatetime.get_dt()).json()
    rainfall = response["items"][0]["readings"][0]["value"]

    # print(type(response.items))
    return rainfall



# for testing reasons:
# def main():
#     temperature = gettemp()
#     print("Temperature:", temperature)
#     rainfall = getrain()
#     print("Rainfall:", rainfall)

# main()