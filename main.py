##############################################
'''
Script to create a Bladed wind file according to a specific pattern.

Usage of this script is without guarantee that this will work.

(c) Galih Bangga, DNV, July 2025
If Bug is found, please contact galih.bangga@dnv.com    
'''

##############################################
# Loading modules
##############################################

import BladedWindCreator as BladedWindCreator 


##############################################
# INPUT DATA
##############################################

# Wind duration
TimeEnd = 300 # in s
TimeStep = 1 # in s


# Gust definition for wind speed
GustTypeSpeed = 'HALF'
GustSpeedStartTime = 50 # in s
GustSpeedEndTime = 125 # in s
GustSpeedStart = 10 # in m/s
GustSpeedAmplitude = 50 # in m/s


# Gust definition for wind direction
GustTypeDir = 'HALF'
GustDirStartTime = 50 # in s
GustDirEndTime = 125 # in s
GustDirStart = 0 # in degrees
GustDirAmplitude = 90 # in degrees


# Wind grid information
Ly = 400 # lateral domain size in m
Lz = 400 # vertical domain size in m
dy = 20 # lateral grid spacing in m
dz = 20 # vertical grid spacing in m


# Calculation of "Start time for turbulent wind" to apply gust at the desired time instance
TowerExtremaLocation = 0 # For jacket model or large support structure, otherwise just zero
NominalRotorDiameter = 120.97
Overhang = 12.03 # Rotor overhang
LateralOffset = 0 # Rotor lateral offset
Floating = "NO" # (NO or YES)
SeaDepth = 0 # Only needed for floating model



OutName = "Wind_ECG_ECD.wnd"

BladedWindCreator.manager.create_wind_file(TimeStep,TimeEnd,
                   GustTypeSpeed,GustSpeedStartTime,GustSpeedEndTime,GustSpeedStart,GustSpeedAmplitude,
                   GustTypeDir,GustDirStartTime,GustDirEndTime,GustDirStart,GustDirAmplitude,
                   Ly,Lz,dy,dz,
                   OutName,
                   TowerExtremaLocation,NominalRotorDiameter,Overhang,LateralOffset,Floating,SeaDepth)













