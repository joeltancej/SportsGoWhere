import numpy as np
import pandas as pd
from math import radians, cos, sin, asin, sqrt

def find_nearest(lat, long, df, field):
    nearest_3 = []
    for i in range(3):
        distances = df.apply(
        lambda row: dist(lat, long, row['lat'], row['lon']), 
        axis=1)
        for j in range(i):
            distances = distances.drop(distances.idxmin())
        if field == "distance":
            nearest_3.append(int(distances.min()*1000))
        else:
            nearest_3.append(df.loc[distances.idxmin(), field])
    return nearest_3

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