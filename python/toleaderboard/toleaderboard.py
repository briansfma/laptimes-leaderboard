##############################################################
# Brian Ma
# To-Leaderboard: Simple lap timer which connects to an online
#                 leaderboard to display top times
#
# To activate, copy everything in this repository into
# "apps/python/toleaderboard/" in your main AC directory.
##############################################################

import sys
import os
import platform
import ac
import acsys

# Fix import path for ctypes (needed for track_times)
if platform.architecture()[0] == "64bit":
    sysdir = 'apps/python/toleaderboard/stdlib64'
else:
    sysdir = 'apps/python/toleaderboard/stdlib'
sys.path.insert(0, sysdir)
os.environ['PATH'] += ";."

# Fix missing imports in Assetto Corsa for socket and unicodedata
import _socket
from unicodedata import ucd_3_2_0 as unicodedata

import urllib.request
import json
import time
from lib.track_times import LaptimeReadout

appWindow = 0
track_times = 0
driver_name = 0
track_name = 0
car_name = 0

def acMain(ac_version):
    global appWindow, track_times
    global driver_name, track_name, car_name

    # Start new application in session
    appWindow = ac.newApp("Laptimes - ToLeaderboard")
    ac.setSize(appWindow, 500, 100)
    
    # Print initial log confirmation
    ac.log(__name__)
    ac.console(__name__)
    
    ac.log("{}".format(sys.path))
    ac.log("{}".format(os.environ))
    
    driver_name = ac.getDriverName(0)
    track_name = ac.getTrackName(0) + ac.getTrackConfiguration(0)
    car_name = ac.getCarName(0)
    
    ac.console("Driver name: {}".format(driver_name))
    ac.console("Track name: {}".format(track_name))
    ac.console("Car name: {}".format(car_name))
    
    # Init individual readouts
    #   Number values are for x/y positioning of readouts if enabled
    track_times = LaptimeReadout(appWindow, 3, 30)
    
    return "Laptimes - ToLeaderboard"

def acUpdate(deltaT):
    global track_times
    global driver_name, track_name, car_name
    
    update_lap, mins, secs, hundredths, avg_speed = track_times.update()
    
    if update_lap:
        lap_formatted = "{:d}:{:02d}.{:02d}".format(mins, secs, hundredths)
        ac.console("Last Lap: " + lap_formatted)
        avg_speed_formatted = "{:04.2f}".format(avg_speed)
        ac.console("Avg Speed: {}".format(avg_speed_formatted))
        
        # Unique identifier for database to ID duplicates
        lapnum = driver_name + str(int(time.time() // 4))
        
        payload = {"user": driver_name,
                   "track": track_name,
                   "vehicle": car_name,
                   "laptime": lap_formatted,
                   "avgspeed": avg_speed_formatted,
                   "lapnum": lapnum}
        
        encoded_data = json.dumps(payload).encode('utf-8')
        
        ac.console("Message encoded: {}".format(encoded_data))
        
        req = urllib.request.Request(url='http://localhost:3000/entries',
                                     data=encoded_data,
                                     headers={'Content-Type': 'application/json'})
                                     
        ac.console("HTTP POST Request created")
        
        try:
            response = urllib.request.urlopen(req)
            ac.console("HTTP response: {}".format(response.getcode()))
        except Exception as e:
            ac.console("Error: {}".format(e))
        
        
        
