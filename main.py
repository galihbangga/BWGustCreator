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
TimeStep = 0.1 # in s
TimeSmooth = 5 # in s, additional time on top of TimeEnd to smooth the wind speeed back to initial value (avoiding instability)


# # Gust definition for wind speed
# GustTypeSpeed = 'HALF'
# GustSpeedStartTime = 10 # in s
# GustSpeedEndTime = 125 # in s
# GustSpeedStart = 10 # in m/s
# GustSpeedAmplitude = 50 # in m/s


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
TowerExtremaLocation = 0 # in m, for jacket model or large support structure, otherwise just zero
NominalRotorDiameter = 241.94 # in m, nominal rotor diameter without cone from Bladed screen
Overhang = 12.03 # in m, rotor overhang
LateralOffset = 0 # in m, rotor lateral offset
Floating = "NO" # (NO or YES)
SeaDepth = 0 # in m, only needed for floating model
InitialNacelleAngle = 0.0 # in degrees, initial nacelle angle set in the model
RotorOrientation = 'UPWIND' # either UPWIND or DOWNWIND
OriginOfWindFileStart = 'HUB' # reference starting point of the wind file, either HUB or GLOBAL


# Output name
OutName = "Wind_ECG_ECD.wnd"



# Output_Directory_Path,LogFilePath,start_execution_time = BladedWindCreator.manager.directory_preparation()
# Time,Speed,Direction,Vel_x,Vel_y,Vel_z,grid_properties = BladedWindCreator.manager.create_gust_1D(LogFilePath,Output_Directory_Path,TimeStep,TimeEnd,TimeSmooth,
#                              GustTypeSpeed,GustSpeedStartTime,GustSpeedEndTime,GustSpeedStart,GustSpeedAmplitude,
#                              GustTypeDir,GustDirStartTime,GustDirEndTime,GustDirStart,GustDirAmplitude,Ly,Lz,dy,dz)
# BladedWindCreator.manager.generate_wind_file(LogFilePath,Output_Directory_Path,OutName,
#                         Time,Speed,Direction,Vel_x,Vel_y,Vel_z,grid_properties,
#                         GustSpeedStart,
#                         TowerExtremaLocation,NominalRotorDiameter,Overhang,LateralOffset,Floating,SeaDepth,InitialNacelleAngle,RotorOrientation,OriginOfWindFileStart,
#                         start_execution_time)



# Wind duration
TimeEnd = 300 # in s
TimeStep = 0.1 # in s
TimeSmooth = 5 # in s, additional time on top of TimeEnd to smooth the wind speeed back to initial value (avoiding instability)

# Gust definition for wind speed
Gust2DSpeedStartTime = 200 # in s
Gust2DSpeedEndTime = 240 # in s
Gust2DSpeedStart = 6 # in m/s
Gust2DRadius = 284 # in m
Gust2DEccentricity = 1 # scale

# Wind grid information
Ly = 400 # lateral domain size in m
Lz = 400 # vertical domain size in m
dy = 5 # lateral grid spacing in m
dz = 5 # vertical grid spacing in m

Output_Directory_Path,LogFilePath,start_execution_time = BladedWindCreator.manager.directory_preparation()
Time,Speed,Direction,Vel_x,Vel_y,Vel_z,grid_properties = BladedWindCreator.manager.create_gust_2D(LogFilePath,Output_Directory_Path,TimeStep,TimeEnd,TimeSmooth,
                             Gust2DSpeedStartTime,Gust2DSpeedEndTime,Gust2DSpeedStart,Gust2DRadius,Gust2DEccentricity,
                             Ly,Lz,dy,dz)
BladedWindCreator.manager.generate_wind_file(LogFilePath,Output_Directory_Path,OutName,
                        Time,Speed,Direction,Vel_x,Vel_y,Vel_z,grid_properties,
                        Gust2DSpeedStart,
                        TowerExtremaLocation,NominalRotorDiameter,Overhang,LateralOffset,Floating,SeaDepth,InitialNacelleAngle,RotorOrientation,OriginOfWindFileStart,
                        start_execution_time)

