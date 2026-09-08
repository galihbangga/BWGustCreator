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

from datetime import datetime
from . import organizer
from . import message
from . import wind_file_creator
from . import gust_creator
from . import wind_shift

# Splash screen
message.splash_start()

###########################################################################
# 
###########################################################################
    

def directory_preparation():
    

    # Log start run time
    start_execution_time = datetime.now()    

    # Creating output directory to store the results
    Output_Directory_Path,LogFilePath = organizer.create_output_directory()
    
    return Output_Directory_Path,LogFilePath,start_execution_time
    
 
def  create_gust_1D(LogFilePath,Output_Directory_Path,TimeStep,TimeEnd,TimeSmooth,
                             GustTypeSpeed,GustSpeedStartTime,GustSpeedEndTime,GustSpeedStart,GustSpeedAmplitude,
                             GustTypeDir,GustDirStartTime,GustDirEndTime,GustDirStart,GustDirAmplitude,Ly,Lz,dy,dz):     
    

    # Create gust timeseries
    Time,Speed,Direction,Vel_x,Vel_y,Vel_z,grid_properties = gust_creator.gust_with_wind_direction_1D(LogFilePath,Output_Directory_Path,TimeStep,TimeEnd,TimeSmooth,
                                 GustTypeSpeed,GustSpeedStartTime,GustSpeedEndTime,GustSpeedStart,GustSpeedAmplitude,
                                 GustTypeDir,GustDirStartTime,GustDirEndTime,GustDirStart,GustDirAmplitude,Ly,Lz,dy,dz)
    
    return Time,Speed,Direction,Vel_x,Vel_y,Vel_z,grid_properties
 
def  create_gust_2D(LogFilePath,Output_Directory_Path,TimeStep,TimeEnd,TimeSmooth,
                             Gust2DSpeedStartTime,Gust2DSpeedEndTime,Gust2DSpeedStart,Gust2DEccentricity,GustCenter_Y,GustCenter_Z,HubHeight,NominalRotorDiameter,
                             Ly,Lz,dy,dz):   
    
    # Create gust timeseries
    Time,Speed,Direction,Vel_x,Vel_y,Vel_z,grid_properties = gust_creator.gust_with_wind_direction_2D(LogFilePath,Output_Directory_Path,TimeStep,TimeEnd,TimeSmooth,
                                 Gust2DSpeedStartTime,Gust2DSpeedEndTime,Gust2DSpeedStart,Gust2DEccentricity,GustCenter_Y,GustCenter_Z,HubHeight,NominalRotorDiameter,
                                 Ly,Lz,dy,dz)
    
    return Time,Speed,Direction,Vel_x,Vel_y,Vel_z,grid_properties 
   
def  generate_wind_file(LogFilePath,Output_Directory_Path,OutName,
                        Time,Speed,Direction,Vel_x,Vel_y,Vel_z,grid_properties,
                        GustSpeedStart,
                        TowerExtremaLocation,NominalRotorDiameter,Overhang,LateralOffset,Floating,SeaDepth,InitialNacelleAngle,RotorOrientation,OriginOfWindFileStart,
                        start_execution_time):
     
    # Generate Bladed wind formatted data
    wind_file_creator.generate_uniform_bladed_wind(LogFilePath,OutName,grid_properties,Vel_x,Vel_y,Vel_z,GustSpeedStart)

    # Calculate information about turbulent buffer time
    wind_shift.buffer_time(LogFilePath,Time,TowerExtremaLocation,NominalRotorDiameter,Overhang,LateralOffset,Floating,SeaDepth,GustSpeedStart,InitialNacelleAngle,RotorOrientation,OriginOfWindFileStart)

    # Splash screen
    message.splash_end()

    # Duration
    end_execution_time = datetime.now()
    execution_time = end_execution_time - start_execution_time 
    
    # Log execution time
    message.log_excecution_time(LogFilePath,start_execution_time,end_execution_time,execution_time)
