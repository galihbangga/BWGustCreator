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

# ==========================================
# General turbine parameters
# ==========================================
# Calculation of "Start time for turbulent wind" to apply gust at the desired time instance
TowerExtremaLocation = 0 # in m, for jacket model or large support structure, otherwise just zero
NominalRotorDiameter = 284 # in m, nominal rotor diameter without cone from Bladed screen
Overhang = 14 # in m, rotor overhang
LateralOffset = 0 # in m, rotor lateral offset
Floating = "NO" # (NO or YES)
SeaDepth = 0 # in m, only needed for floating model
InitialNacelleAngle = 0.0 # in degrees, initial nacelle angle set in the model
RotorOrientation = 'UPWIND' # either UPWIND or DOWNWIND
OriginOfWindFileStart = 'HUB' # reference starting point of the wind file, either HUB or GLOBAL
HubHeight = 170 # Set this value as the location of wind file center in Bladed simulation




# ==========================================  EXAMPLE 1D GUST ==========================================

# # Wind duration
# TimeEnd = 300 # in s
# TimeStep = 0.1 # in s
# TimeSmooth = 5 # in s, last part of TimeEnd replaced by a linear ramp back to the initial value (avoiding instability)

# # Gust definition for wind speed
# GustTypeSpeed = 'HALF'
# GustSpeedStartTime = 10 # in s
# GustSpeedEndTime = 125 # in s
# GustSpeedStart = 10 # in m/s
# GustSpeedAmplitude = 50 # in m/s


# # Gust definition for wind direction
# GustTypeDir = 'HALF'
# GustDirStartTime = 50 # in s
# GustDirEndTime = 125 # in s
# GustDirStart = 0 # in degrees
# GustDirAmplitude = 90 # in degrees


# # Wind grid information
# Ly = 400 # lateral domain size in m
# Lz = 400 # vertical domain size in m
# dy = 5 # lateral grid spacing in m
# dz = 5 # vertical grid spacing in m



# # Output name
# OutName = "Wind_ECG_ECD_1D.wnd"



# # Code calls

# Output_Directory_Path,LogFilePath,start_execution_time = BladedWindCreator.manager.directory_preparation()
# Time,Speed,Direction,Vel_x,Vel_y,Vel_z,grid_properties = BladedWindCreator.manager.create_gust_1D(LogFilePath,Output_Directory_Path,TimeStep,TimeEnd,TimeSmooth,
#                               GustTypeSpeed,GustSpeedStartTime,GustSpeedEndTime,GustSpeedStart,GustSpeedAmplitude,
#                               GustTypeDir,GustDirStartTime,GustDirEndTime,GustDirStart,GustDirAmplitude,Ly,Lz,dy,dz)
# BladedWindCreator.manager.generate_wind_file(LogFilePath,Output_Directory_Path,OutName,
#                         Time,Speed,Direction,Vel_x,Vel_y,Vel_z,grid_properties,
#                         GustSpeedStart,
#                         TowerExtremaLocation,NominalRotorDiameter,Overhang,LateralOffset,Floating,SeaDepth,InitialNacelleAngle,RotorOrientation,OriginOfWindFileStart,
#                         start_execution_time)



# ==========================================  EXAMPLE 2D CIRCULAR GUST ==========================================

# Wind duration
TimeEnd = 300 # in s
TimeStep = 0.1 # in s
TimeSmooth = 5 # in s, last part of TimeEnd replaced by a linear ramp back to the initial value (avoiding instability)

# Gust definition for wind speed
GustTypeSpeed = 'HALF' # 'HALF', 'FULL' or 'IEC'
GustSpeedStartTime = 100 # in s
GustSpeedEndTime = 200 # in s
GustSpeedStart = 6 # in m/s
GustSpeedAmplitude = 5 # in m/s
GustRadius = 100 # in m
GustCenter_Y = 50 # in m, measured from center of grid
GustCenter_Z = (90-HubHeight) # in m, measured from center of grid

# Gust definition for wind direction
GustTypeDir = "HALF"
GustDirStartTime = 100 # in s
GustDirEndTime = 200 # in s
GustDirStart = 0 # in deg
GustDirAmplitude = 90 # in deg

# Wind grid information
Ly = 400 # lateral domain size in m
Lz = 400 # vertical domain size in m
dy = 5 # lateral grid spacing in m
dz = 5 # vertical grid spacing in m

# Output name
OutName = "Wind_2DGust_Circular.wnd"

# Code calls
Output_Directory_Path,LogFilePath,start_execution_time = BladedWindCreator.manager.directory_preparation()
Time,Speed,Direction,Vel_x,Vel_y,Vel_z,grid_properties = BladedWindCreator.manager.create_gust_2D_circular(LogFilePath,Output_Directory_Path,TimeStep,TimeEnd,TimeSmooth,
                              GustTypeSpeed,GustSpeedStartTime,GustSpeedEndTime,GustSpeedStart,GustSpeedAmplitude,
                              GustRadius,GustCenter_Y,GustCenter_Z,HubHeight,NominalRotorDiameter,
                              GustTypeDir,GustDirStartTime,GustDirEndTime,GustDirStart,GustDirAmplitude,
                              Ly,Lz,dy,dz)
BladedWindCreator.manager.generate_wind_file(LogFilePath,Output_Directory_Path,OutName,
                        Time,Speed,Direction,Vel_x,Vel_y,Vel_z,grid_properties,
                        GustSpeedStart,
                        TowerExtremaLocation,NominalRotorDiameter,Overhang,LateralOffset,Floating,SeaDepth,InitialNacelleAngle,RotorOrientation,OriginOfWindFileStart,
                        start_execution_time)



# ==========================================  EXAMPLE 2D IEA Wind Task 47 GUST - COHERENT ==========================================


# # Wind duration
# TimeEnd = 300 # in s
# TimeStep = 0.1 # in s
# TimeSmooth = 5 # in s, gust rise/fall time and last part of TimeEnd replaced by a linear ramp back to the initial value (avoiding instability)

# # Gust definition for wind speed
# Gust2DSpeedStartTime = 200 # in s
# Gust2DSpeedEndTime = 240 # in s
# Gust2DSpeedStart = 6 # in m/s
# Gust2DEccentricity = 1/500 # scale
# GustCenter_Y = 0 # in m, measured from center of grid
# GustCenter_Z = 0 # in m, measured from center of grid

# # Gust definition for wind direction
# GustTypeDir = 'IEC'
# GustDirStartTime = 200 # in s
# GustDirEndTime = 240 # in s
# GustDirStart = 0 # in degrees
# GustDirAmplitude = 10 # in degrees

# # Wind grid information
# Ly = 400 # lateral domain size in m
# Lz = 400 # vertical domain size in m
# dy = 5 # lateral grid spacing in m
# dz = 5 # vertical grid spacing in m


# # Output name
# OutName = "Wind_2DGust_IEATask47_Coherent.wnd"


# # Code calls

# Output_Directory_Path,LogFilePath,start_execution_time = BladedWindCreator.manager.directory_preparation()
# Time,Speed,Direction,Vel_x,Vel_y,Vel_z,grid_properties = BladedWindCreator.manager.create_gust_2D_IEAWind47(LogFilePath,Output_Directory_Path,TimeStep,TimeEnd,TimeSmooth,
#                               Gust2DSpeedStartTime,Gust2DSpeedEndTime,Gust2DSpeedStart,Gust2DEccentricity,GustCenter_Y,GustCenter_Z,HubHeight,NominalRotorDiameter,
#                               GustTypeDir,GustDirStartTime,GustDirEndTime,GustDirStart,GustDirAmplitude,
#                               Ly,Lz,dy,dz)
# BladedWindCreator.manager.generate_wind_file(LogFilePath,Output_Directory_Path,OutName,
#                         Time,Speed,Direction,Vel_x,Vel_y,Vel_z,grid_properties,
#                         Gust2DSpeedStart,
#                         TowerExtremaLocation,NominalRotorDiameter,Overhang,LateralOffset,Floating,SeaDepth,InitialNacelleAngle,RotorOrientation,OriginOfWindFileStart,
#                         start_execution_time)




# ==========================================  EXAMPLE 2D IEA Wind Task 47 GUST - INCOHERENT ==========================================


# # Wind duration
# TimeEnd = 300 # in s
# TimeStep = 0.1 # in s
# TimeSmooth = 5 # in s, gust rise/fall time and last part of TimeEnd replaced by a linear ramp back to the initial value (avoiding instability)

# # Gust definition for wind speed
# Gust2DSpeedStartTime = 50 # in s
# Gust2DSpeedEndTime = 200 # in s
# Gust2DSpeedStart = 10 # in m/s
# Gust2DEccentricity = 3/430 # scale

# # in m, measured from center of grid, 
# # HubHeight is hub height where the center of the wind file will be placed in Bladed simulation
# # For example, if gust is to be centered at 90 m from the "ground", GustCenter_Z measured from grid center (hub height) will be
# # 90 - HubHeight
# GustCenter_Y = 0 # in m, measured from center of grid
# GustCenter_Z = (90-HubHeight) 

# # Gust definition for wind direction
# GustTypeDir = "HALF"
# GustDirStartTime = 50 # in s
# GustDirEndTime = 200 # in s
# GustDirStart = 0 # in deg
# GustDirAmplitude = 90 # in deg

# # Wind grid information
# Ly = 400 # lateral domain size in m
# Lz = 400 # vertical domain size in m
# dy = 5 # lateral grid spacing in m
# dz = 5 # vertical grid spacing in m


# # Output name
# OutName = "Wind_2DGust_IEATask47_InCoherent.wnd"


# # Code calls

# Output_Directory_Path,LogFilePath,start_execution_time = BladedWindCreator.manager.directory_preparation()
# Time,Speed,Direction,Vel_x,Vel_y,Vel_z,grid_properties = BladedWindCreator.manager.create_gust_2D_IEAWind47(LogFilePath,Output_Directory_Path,TimeStep,TimeEnd,TimeSmooth,
#                               Gust2DSpeedStartTime,Gust2DSpeedEndTime,Gust2DSpeedStart,Gust2DEccentricity,GustCenter_Y,GustCenter_Z,HubHeight,NominalRotorDiameter,
#                               GustTypeDir,GustDirStartTime,GustDirEndTime,GustDirStart,GustDirAmplitude,
#                               Ly,Lz,dy,dz)
# BladedWindCreator.manager.generate_wind_file(LogFilePath,Output_Directory_Path,OutName,
#                         Time,Speed,Direction,Vel_x,Vel_y,Vel_z,grid_properties,
#                         Gust2DSpeedStart,
#                         TowerExtremaLocation,NominalRotorDiameter,Overhang,LateralOffset,Floating,SeaDepth,InitialNacelleAngle,RotorOrientation,OriginOfWindFileStart,
#                         start_execution_time)












