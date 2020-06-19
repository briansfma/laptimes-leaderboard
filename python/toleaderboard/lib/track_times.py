# Script to handle acquisition of best/last/current lap data

import ac
import acsys

from sim_info import info

# Parameters
tireOffLimit = 3

class LaptimeReadout:
    def __init__(self, appWindow, x, y):
        # Init containers
        self.lapCount = 0
        self.bestLap = 0
        self.bestLapNum = 0
        self.lastLap = 0
        self.currentLap = 0
        self.lapValid = True
        self.odometer = 0
        self.last_odometer = 0
        
        ac.console("Lap valid? {}".format(self.lapValid))

        # Init and display labels for best, last and current lap
        self.l_bestLap = ac.addLabel(appWindow, "Best Lap: 0:00.00");
        ac.setPosition(self.l_bestLap, x, y)
        self.l_lastLap = ac.addLabel(appWindow, "Last Lap: 0:00.00");
        ac.setPosition(self.l_lastLap, x+150, y)
        self.l_currentLap = ac.addLabel(appWindow, "Current Lap: 0:00.00 (I)");
        ac.setPosition(self.l_currentLap, x+300, y)
    
    def convertMS(self, millis):
        hundredths = int((millis/10)%100)
        seconds = int((millis/1000)%60)
        minutes = int(millis/(1000*60))
        
        return minutes, seconds, hundredths
    
    def update(self):
        # Constantly monitor if car has cut the track (lap invalid)
        global tireOffLimit
        offTrack = info.physics.numberOfTyresOut > tireOffLimit
        if offTrack:
            self.lapValid = False
            ac.console("Lap valid? {}".format(self.lapValid))
        
        # Track how much distance the car has covered (avg speed calc)
        self.odometer = info.graphics.distanceTraveled
        
        # Get and update current lap time
        self.currentLap = ac.getCarState(0, acsys.CS.LapTime)
        mins, secs, hundredths = self.convertMS(self.currentLap)
        
        ac.setText(self.l_currentLap, 
                   "Current Lap: {:d}:{:02d}.{:02d} ({})"
                   .format(mins, secs, hundredths, self.lapValid))
        
        # Update lap count only when it happens
        laps = ac.getCarState(0, acsys.CS.LapCount)
        if (laps > self.lapCount):
            update_lap = self.lapValid
        
            self.lapCount = laps
            
            self.lastLap = ac.getCarState(0, acsys.CS.LastLap)
            mins, secs, hundredths = self.convertMS(self.lastLap)
                    
            ac.setText(self.l_lastLap, 
                       "Last Lap: {:d}:{:02d}.{:02d} ({})"
                       .format(mins, secs, hundredths, self.lapValid))
            
            # Count distance covered in lap, reset counter
            dist_traveled = self.odometer - self.last_odometer
            avg_speed = dist_traveled / self.lastLap * 2236.94# m/ms to mph
            self.last_odometer = self.odometer
            
            # Compare last lap to best lap only if valid
            if ((self.lastLap < self.bestLap or self.bestLap == 0)
              and self.lapValid):
                self.bestLapNum = laps
                self.bestLap = self.lastLap
                
                ac.setText(self.l_bestLap, 
                           "Best Lap: {:d}:{:02d}.{:02d} ({:d})"
                           .format(mins, secs, hundredths, self.bestLapNum))
            
            # New lap, new chance for valid lap
            self.lapValid = True
        
            return update_lap, mins, secs, hundredths, avg_speed
        
        else:
            return False, 0, 0, 0, 0

