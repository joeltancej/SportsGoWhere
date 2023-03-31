import pandas as pd
from NearestFinder.findNearest import *
import mysql.connector as connection
from NearestFinder.chatbot import *
# this function returns a dictionary containing the information of the nearest 3 carparks
# the information for every carpark is contained in a dictionary containing the address, carpark number (needed for carpark API),
# and the distance (in metres) from the particular location (lat, long) to the carpark

def nearestHE(lat, long):
    # replace password with your own password here
    try:
        mydb = connection.connect(host="localhost", database = 'sportsgowhere',user="root", passwd="password",use_pure=True)
        query = "Select * from healthiereateries;"
        healthiereateries = pd.read_sql(query,mydb)
        mydb.close() #close the connection
    except Exception as e:
        mydb.close()
        print(str(e))

    # getting carparks dataset as a dataframe
    # hdbcarparks = pd.read_excel("Datasets/hdbcarparks(converted).xlsx")
    # Renaming the column names 
    healthiereateries=healthiereateries.rename(columns = {'Y':'lat','X':'lon'})
    nearestname = find_nearest(lat, long, healthiereateries, "Name" )
    nearestlat = find_nearest(lat, long, healthiereateries, "lat" )
    nearestlon = find_nearest(lat, long, healthiereateries, "lon" )
    # healthieroptions = []
    # for name in nearestname:
    #     query = "What healthy options are there at" + name + " Singapore? Answer in at most 50 words. If you face difficulties answering, simply reply me with 'Information currently unavailable'"
    #     healthieroptions.append(chatgpt(query))
    # nearestblk = find_nearest(lat, long, healthiereateries, "ADDRESSBLOCKHOUSENUMBER" )
    # nearestbld = find_nearest(lat, long, healthiereateries, "ADDRESSBUILDINGNAME" )
    # nearestpos = find_nearest(lat, long, healthiereateries, "ADDRESSPOSTALCODE" )
    nearestst = find_nearest(lat, long, healthiereateries, "ADDRESSSTREETNAME" )
    nearestdist = find_nearest(lat, long, healthiereateries, "distance" )
    nearestdesc = find_nearest(lat, long, healthiereateries, "description" )
    result = {"first":{"name":nearestname[0], "dist":nearestdist[0], "lat":nearestlat[0], "lon":nearestlon[0], "healthieroptions":nearestdesc[0], "st":nearestst[0]},
              "second":{"name":nearestname[1], "dist":nearestdist[1], "lat":nearestlat[1], "lon":nearestlon[1], "healthieroptions":nearestdesc[1], "st":nearestst[1]},
              "third":{"name":nearestname[2], "dist":nearestdist[2], "lat":nearestlat[2], "lon":nearestlon[2], "healthieroptions":nearestdesc[2], "st":nearestst[2]}}
    
    return result
    
#     for testing purposes
    

# nearestCP(103.93721, 1.35961)