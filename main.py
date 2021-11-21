import pandas as pd
import matplotlib.pyplot as plt
import datetime
from math import radians, cos, sin, asin, sqrt
from scipy import interpolate
import numpy as np
from statistics import mean
import scipy.signal as sig

dfGps = pd.read_csv('track.csv')

time = dfGps['time'].values
lat = dfGps['lat'].values
lon = dfGps['lon'].values
evl = dfGps['ele'].values
print('Time column', time)
print('Latitue column', lat)
print('Longitute column', lon)
print('Elevation column', evl)
plt.title("Logtitude vs Latitude Plot")
plt.plot(lon,lat,'-r')
plt.show()

timeDifferences = []
for i in range(1, len(time)):
    time1Str = str(time[i-1])
    time2Str = str(time[i])
    time1Obj = datetime.datetime.strptime(time1Str, '%Y-%m-%d %H:%M:%S+00:00')
    time2Obj = datetime.datetime.strptime(time2Str,'%Y-%m-%d %H:%M:%S+00:00')
    timeDiff = time2Obj - time1Obj
    timeDifferences.append(timeDiff.seconds)
print("Time Differences: ",timeDifferences)
plt.title("Time Differences Plot")
plt.plot(timeDifferences)
plt.show()



def haversine(lon1, lat1, lon2, lat2):
    # convert decimal degrees to radians
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    r = 6371 # Radius of earth in kilometers. Use 3956 for miles
    return c * r
distances = []
for i in range(1,len(lat)):
    distances.append(haversine(lon[i-1], lat[i-1], lon[i], lat[i]))
print("Distances using haversine formula:",distances)


speed = [i / j for i, j in zip(distances, timeDifferences)]
print("Speed array: ",speed)


timeDifferences.append(1)
latInter = interpolate.interp1d(timeDifferences, lat)
lonInter = interpolate.interp1d(timeDifferences, lon)
evlInter = interpolate.interp1d(timeDifferences, evl)
latInterpo = latInter(timeDifferences)
lonInterpo = lonInter(timeDifferences)
plt.title("Graph of Interpolated Points")
plt.plot(lat, lon, 'o', latInterpo, lonInterpo, '-rx')
plt.show()
distancesInter = []
for i in range(1,len(lat)):
    distancesInter.append(haversine(lon[i-1], lat[i-1], lon[i], lat[i]))


speedInter = [i / j for i, j in zip(distancesInter, timeDifferences)]
print("Speed form interpolated data: ",speedInter)


evlDiff = []
for i in range(1,len(evl)):
    evlDiff.append(abs(evl[i-1]-evl[i]))
print("Elevation Differences: ", evlDiff)

e = []
for i in evlDiff:
    e.append(i*9.8*100)
print("Power output or E: ", e)

plt.title("Graph of E as function of time span")
plt.plot(distancesInter,e)
plt.show()


average_power = mean(e)
power_loss = average_power - 160
print("Power loss: ",round(power_loss))


[b,a] = sig.butter(2,0.01)
eleFiltered = sig.lfilter(b,a,evl)
average_power = mean(eleFiltered)
power_loss = abs(average_power - 160)
print("Power loss(filtered E): ",round(power_loss))