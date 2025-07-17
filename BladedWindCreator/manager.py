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

###########################################################################
# 
###########################################################################
    

def create_wind_file(TimeStep,TimeEnd,
                   GustTypeSpeed,GustSpeedStartTime,GustSpeedEndTime,GustSpeedStart,GustSpeedAmplitude,
                   GustTypeDir,GustDirStartTime,GustDirEndTime,GustDirStart,GustDirAmplitude,
                   Ly,Lz,dy,dz,
                   OutName,
                   TowerExtremaLocation,NominalRotorDiameter,Overhang,LateralOffset,Floating,SeaDepth):
    
    
    
    # Splash screen
    message.splash_start()


    # Log start run time
    start_execution_time = datetime.now()    

    # Creating output directory to store the results
    Output_Directory_Path,LogFilePath = organizer.create_output_directory()
    
    # Create gust timeseries
    Time,Speed,Direction,Vel_x,Vel_y,Vel_z = gust_creator.gust_with_wind_direction(LogFilePath,Output_Directory_Path,TimeStep,TimeEnd,
                                 GustTypeSpeed,GustSpeedStartTime,GustSpeedEndTime,GustSpeedStart,GustSpeedAmplitude,
                                 GustTypeDir,GustDirStartTime,GustDirEndTime,GustDirStart,GustDirAmplitude)
    
    # Generate Bladed wind formatted data
    grid_properties = wind_file_creator.collect_grid_info(LogFilePath,Ly,Lz,dy,dz,TimeEnd,TimeStep,GustSpeedStart)
    wind_file_creator.generate_uniform_bladed_wind(LogFilePath,OutName,grid_properties,Vel_x,Vel_y,Vel_z,GustSpeedStart)

    # Calculate information about turbulent buffer time
    wind_file_creator.buffer_time(LogFilePath,TimeEnd,TowerExtremaLocation,NominalRotorDiameter,Overhang,LateralOffset,Floating,SeaDepth,GustSpeedStart)

    # Splash screen
    message.splash_end()

    # Duration
    end_execution_time = datetime.now()
    execution_time = end_execution_time - start_execution_time 
    
    # Log execution time
    message.log_excecution_time(LogFilePath,start_execution_time,end_execution_time,execution_time)
