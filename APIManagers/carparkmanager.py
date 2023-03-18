# import requests library to make requests and work with API
import requests
# import from sgdatetime to get the SGT parameters
import sgdatetime

def getcarparkdata():
    # making a GET request to the API endpoint, obtain output in a dictionary format with .json()
    response = requests.get("https://api.data.gov.sg/v1/transport/carpark-availability", sgdatetime.get_dt()).json()
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

# for testing reasons:
def main():
    carpark = getcarparkinfo("TM31")
    print(carpark)

main()