# import requests library to make requests and work with API
import requests
# import from sgdatetime to get the SGT parameters
import sgdatetime

def getcarpark():
    # making a GET request to the API endpoint, obtain output in a dictionary format with .json()
    response = requests.get("https://api.data.gov.sg/v1/transport/carpark-availability", sgdatetime.get_dt()).json()
    # psi = response["items"][0]["readings"]["psi_twenty_four_hourly"][region]

    # print(type(response.items))
    return response

# for testing reasons:
def main():
    carpark = getcarpark()
    print(carpark)

main()