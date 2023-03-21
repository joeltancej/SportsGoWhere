import pandas as pd
from NearestFinder.findNearest import *
import mysql.connector as connection
# this function returns a dictionary containing the information of the nearest 3 carparks
# the information for every carpark is contained in a dictionary containing the address, carpark number (needed for carpark API),
# and the distance (in metres) from the particular location (lat, long) to the carpark

def nearestCP(lat, long):
    # replace password with your own password here
    try:
        mydb = connection.connect(host="localhost", database = 'sportsgowhere',user="root", passwd="Wushurocks1!",use_pure=True)
        query = "Select * from healthiereateries;"
        healthiereateries = pd.read_sql(query,mydb)
        mydb.close() #close the connection
    except Exception as e:
        mydb.close()
        print(str(e))

    # getting carparks dataset as a dataframe
    # hdbcarparks = pd.read_excel("Datasets/hdbcarparks(converted).xlsx")
    # Renaming the column names 
    healthiereateries=healthiereateries.rename(columns = {'X':'lat','Y':'lon'})
    nearestname = find_nearest(lat, long, healthiereateries, "Name" )
    nearestblk = find_nearest(lat, long, healthiereateries, "ADDRESSBLOCKHOUSENUMBER" )
    nearestbld = find_nearest(lat, long, healthiereateries, "ADDRESSBUILDINGNAME" )
    nearestpos = find_nearest(lat, long, healthiereateries, "ADDRESSPOSTALCODE" )
    nearestst = find_nearest(lat, long, healthiereateries, "ADDRESSSTREETNAME" )
    result = {"first":{"name":nearestname[0], "blk":nearestblk[0], "bld":nearestbld[0], "pos":nearestpos[0], "st":nearestst[0]},
              "second":{"name":nearestname[1], "cpno":nearestblk[1], "bld":nearestbld[1], "pos":nearestpos[1], "st":nearestst[1]},
              "third":{"name":nearestname[2], "blk":nearestblk[2], "bld":nearestbld[2]}, "pos":nearestpos[2], "st":nearestst[2]}
    for i in range(3):
        print(nearestname[i], end=" ")
        print(nearestblk[i], end=" ")
        print(nearestbld[i], end=" ")
        print(nearestpos[i], end=" ")
        print(nearestst[i])
    return result
    
#     for testing purposes
    

nearestCP(103.93721, 1.35961)