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
    '''
    Prepare the output environment for a new run.

    Creates the output directory together with its log file and records
    the start time of the execution.

    Returns
    Output_Directory_Path : directory where all results and figures are stored
    LogFilePath           : path of the log file created inside the output directory
    start_execution_time  : datetime stamp marking the beginning of the run
    '''

    # Log start run time
    start_execution_time = datetime.now()    

    # Creating output directory to store the results
    Output_Directory_Path,LogFilePath = organizer.create_output_directory()
    
    return Output_Directory_Path,LogFilePath,start_execution_time
    
 
def  create_gust_1D(LogFilePath,Output_Directory_Path,TimeStep,TimeEnd,TimeSmooth,
                             GustTypeSpeed,GustSpeedStartTime,GustSpeedEndTime,GustSpeedStart,GustSpeedAmplitude,
                             GustTypeDir,GustDirStartTime,GustDirEndTime,GustDirStart,GustDirAmplitude,Ly,Lz,dy,dz):     
    '''
    Wrapper creating a 1-dimensional gust (uniform over the grid plane) in both
    wind speed and wind direction.

    LogFilePath           : path of the log file, appended with the gust information
    Output_Directory_Path : directory where the figures are saved
    TimeStep              : time step [s] of the wind file
    TimeEnd               : target end time [s] of the gust signal, before smoothing
    TimeSmooth            : duration [s] of the linear ramp appended after TimeEnd
    GustTypeSpeed         : gust shape for wind speed ("HALF" or "IEC")
    GustSpeedStartTime    : start time [s] of the wind speed gust
    GustSpeedEndTime      : end time [s] of the wind speed gust
    GustSpeedStart        : baseline wind speed [m/s]
    GustSpeedAmplitude    : wind speed gust amplitude [m/s]
    GustTypeDir           : gust shape for wind direction ("HALF" or "IEC")
    GustDirStartTime      : start time [s] of the wind direction gust
    GustDirEndTime        : end time [s] of the wind direction gust
    GustDirStart          : baseline wind direction [deg]
    GustDirAmplitude      : wind direction gust amplitude [deg]
    Ly, Lz                : lateral and vertical extent [m] of the wind grid
    dy, dz                : lateral and vertical grid spacing [m]

    Returns
    Time            : 1D array of time [s], size (nt,)
    Speed           : 3D array of wind speed magnitude [m/s], shape (nt, ny, nz)
    Direction       : 3D array of wind direction [deg], shape (nt, ny, nz)
    Vel_x           : 3D array of longitudinal velocity [m/s], shape (nt, ny, nz)
    Vel_y           : 3D array of lateral velocity [m/s], shape (nt, ny, nz)
    Vel_z           : 3D array of vertical velocity [m/s], shape (nt, ny, nz)
    grid_properties : tuple (dx,dy,dz,num_x,num_y,num_z) describing the wind grid
    '''

    # Create gust timeseries
    Time,Speed,Direction,Vel_x,Vel_y,Vel_z,grid_properties = gust_creator.gust_with_wind_direction_1D(LogFilePath,Output_Directory_Path,TimeStep,TimeEnd,TimeSmooth,
                                 GustTypeSpeed,GustSpeedStartTime,GustSpeedEndTime,GustSpeedStart,GustSpeedAmplitude,
                                 GustTypeDir,GustDirStartTime,GustDirEndTime,GustDirStart,GustDirAmplitude,Ly,Lz,dy,dz)
    
    return Time,Speed,Direction,Vel_x,Vel_y,Vel_z,grid_properties
 
def  create_gust_2D(LogFilePath,Output_Directory_Path,TimeStep,TimeEnd,TimeSmooth,
                             Gust2DSpeedStartTime,Gust2DSpeedEndTime,Gust2DSpeedStart,Gust2DEccentricity,GustCenter_Y,GustCenter_Z,HubHeight,NominalRotorDiameter,
                             GustTypeDir,GustDirStartTime,GustDirEndTime,GustDirStart,GustDirAmplitude,
                             Ly,Lz,dy,dz):   
    '''
    Wrapper creating a 2-dimensional gust, i.e. a localised velocity excess with a
    radial spatial shape in the Y-Z plane and a trapezoidal time evolution.

    LogFilePath           : path of the log file, appended with the gust information
    Output_Directory_Path : directory where the figures are saved
    TimeStep              : time step [s] of the wind file
    TimeEnd               : end time [s] of the wind file
    TimeSmooth            : ramp-up/ramp-down duration [s] of the gust in time
    Gust2DSpeedStartTime  : time [s] at which the gust reaches its full magnitude
    Gust2DSpeedEndTime    : time [s] at which the gust starts to decay
    Gust2DSpeedStart      : baseline (uniform) wind speed [m/s]
    Gust2DEccentricity    : inverse spatial extent [1/m] of the gust; larger values
                            give a smaller and sharper gust core
    GustCenter_Y          : lateral offset [m] of the gust center from the grid center
    GustCenter_Z          : vertical offset [m] of the gust center from the grid center
    HubHeight             : hub height [m], used to reference the grid to absolute height
    NominalRotorDiameter  : rotor diameter [m], drawn as a reference circle in the contour plot
    GustTypeDir            : gust shape for wind direction ("HALF" or "IEC")
    GustDirStartTime       : start time [s] of the wind direction gust
    GustDirEndTime         : end time [s] of the wind direction gust
    GustDirStart           : baseline wind direction [deg]
    GustDirAmplitude       : wind direction gust amplitude [deg]
    Ly, Lz                : lateral and vertical extent [m] of the wind grid
    dy, dz                : lateral and vertical grid spacing [m]

    Returns
    Time            : 1D array of time [s], size (nt,)
    Speed           : 3D array of wind speed magnitude [m/s], shape (nt, ny, nz)
    Direction       : 3D array of wind direction [deg], shape (nt, ny, nz)
    Vel_x           : 3D array of longitudinal velocity [m/s], shape (nt, ny, nz)
    Vel_y           : 3D array of lateral velocity [m/s], shape (nt, ny, nz)
    Vel_z           : 3D array of vertical velocity [m/s], shape (nt, ny, nz)
    grid_properties : tuple (dx,dy,dz,num_x,num_y,num_z) describing the wind grid
    '''

    # Create gust timeseries
    Time,Speed,Direction,Vel_x,Vel_y,Vel_z,grid_properties = gust_creator.gust_with_wind_direction_2D(LogFilePath,Output_Directory_Path,TimeStep,TimeEnd,TimeSmooth,
                                 Gust2DSpeedStartTime,Gust2DSpeedEndTime,Gust2DSpeedStart,Gust2DEccentricity,GustCenter_Y,GustCenter_Z,HubHeight,NominalRotorDiameter,
                                 GustTypeDir,GustDirStartTime,GustDirEndTime,GustDirStart,GustDirAmplitude,
                                 Ly,Lz,dy,dz)
    
    return Time,Speed,Direction,Vel_x,Vel_y,Vel_z,grid_properties 
   
def  generate_wind_file(LogFilePath,Output_Directory_Path,OutName,
                        Time,Speed,Direction,Vel_x,Vel_y,Vel_z,grid_properties,
                        GustSpeedStart,
                        TowerExtremaLocation,NominalRotorDiameter,Overhang,LateralOffset,Floating,SeaDepth,InitialNacelleAngle,RotorOrientation,OriginOfWindFileStart,
                        start_execution_time):
    '''
    Write the Bladed wind file, report the turbulence buffer time and close the run log.

    LogFilePath           : path of the log file, appended with the run information
    Output_Directory_Path : directory where all results are stored
    OutName               : file name of the generated Bladed wind file
    Time                  : 1D array of time [s], size (nt,)
    Speed                 : 3D array of wind speed magnitude [m/s], shape (nt, ny, nz)
    Direction             : 3D array of wind direction [deg], shape (nt, ny, nz)
    Vel_x                 : 3D array of longitudinal velocity [m/s], shape (nt, ny, nz)
    Vel_y                 : 3D array of lateral velocity [m/s], shape (nt, ny, nz)
    Vel_z                 : 3D array of vertical velocity [m/s], shape (nt, ny, nz)
    grid_properties       : tuple (dx,dy,dz,num_x,num_y,num_z) describing the wind grid
    GustSpeedStart        : baseline wind speed [m/s], used as the normalisation mean speed
    TowerExtremaLocation  : most upwind/downwind tower station location [m]
    NominalRotorDiameter  : rotor diameter [m]
    Overhang              : distance [m] from the tower axis to the rotor apex
    LateralOffset         : lateral offset [m] of the rotor from the tower axis
    Floating              : flag indicating whether the turbine is floating
    SeaDepth              : water depth [m], relevant for floating turbines
    InitialNacelleAngle   : initial nacelle yaw angle [deg]
    RotorOrientation      : rotor configuration (upwind or downwind)
    OriginOfWindFileStart : reference origin used for the wind file start position
    start_execution_time  : datetime stamp marking the beginning of the run

    Returns
    None
    '''

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
