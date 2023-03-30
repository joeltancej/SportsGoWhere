import numpy as np
import pandas as pd
from NearestFinder.findNearest import *
import mysql.connector as connection
# this function returns a dictionary containing the information of the nearest 3 carparks
# the information for every carpark is contained in a dictionary containing the address, carpark number (needed for carpark API),
# and the distance (in metres) from the particular location (lat, long) to the carpark

def nearestCP(lat, long):
    # replace password with your own password here
    try:
        mydb = connection.connect(host="localhost", database = 'sportsgowhere',user="root", passwd="password",use_pure=True)
        query = "Select * from hdbcarparks;"
        hdbcarparks = pd.read_sql(query,mydb)
        mydb.close() #close the connection
    except Exception as e:
        mydb.close()
        print(str(e))

    # getting carparks dataset as a dataframe
    # hdbcarparks = pd.read_excel("Datasets/hdbcarparks(converted).xlsx")
    # Renaming the column names 
    hdbcarparks=hdbcarparks.rename(columns = {'x':'lat','y':'lon'})
    nearestadd = find_nearest(lat, long, hdbcarparks, "address" )
    nearestcpno = find_nearest(lat, long, hdbcarparks, "car_park_no" )
    nearestdist = find_nearest(lat, long, hdbcarparks, "distance" )
    result = {"first":{"address":nearestadd[0], "cpno":nearestcpno[0], "dist":nearestdist[0], "duration":round(nearestdist[0]/(1.4*60))},
              "second":{"address":nearestadd[1], "cpno":nearestcpno[1], "dist":nearestdist[1], "duration":round(nearestdist[1]/(1.4*60))},
              "third":{"address":nearestadd[2], "cpno":nearestcpno[2], "dist":nearestdist[2], "duration":round(nearestdist[2]/(1.4*60))}}
    
    return result
    
#     for testing purposes
    

# nearestCP(103.93721, 1.35961)