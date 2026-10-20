##############################################
'''
Script to create a Bladed wind file according to a specific pattern.

Usage of this script is without guarantee that this will work.

(c) Galih Bangga, DNV, July 2025
If Bug is found, please contact galih.bangga@dnv.com    
'''
##############################################


##############################################
# Loading modules
##############################################

import numpy as np
from .. import wind_file_creator
from . import gust_shapes
from . import gust_plots

##############################################



def gust_with_wind_direction_1D(LogFilePath,Output_Directory_Path,TimeStep,TimeEnd,TimeSmooth,
                             GustTypeSpeed,GustSpeedStartTime,GustSpeedEndTime,GustSpeedStart,GustSpeedAmplitude,
                             GustTypeDir,GustDirStartTime,GustDirEndTime,GustDirStart,GustDirAmplitude,Ly,Lz,dy,dz):
    '''
    Build a 1-dimensional (uniform over the grid plane) gust in both wind speed and
    wind direction, expand it over the 3D wind grid and generate the diagnostic plots.

    LogFilePath           : path of the log file, appended with the gust information
    Output_Directory_Path : directory where the figures are saved
    TimeStep              : time step [s] of the wind file
    TimeEnd               : end time [s] of the wind file
    TimeSmooth            : duration [s] of the linear ramp at the end of the wind file (within TimeEnd)
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
    Time_Smoothed   : 1D array of time [s], size (nt,)
    Speed_array     : 3D array of wind speed magnitude [m/s], shape (nt, ny, nz)
    Direction_array : 3D array of wind direction [deg], shape (nt, ny, nz)
    u_array         : 3D array of longitudinal velocity [m/s], shape (nt, ny, nz)
    v_array         : 3D array of lateral velocity [m/s], shape (nt, ny, nz)
    w_array         : 3D array of vertical velocity [m/s], shape (nt, ny, nz)
    grid_properties : tuple (dx,dy,dz,num_x,num_y,num_z) describing the wind grid
    '''

    print(" One-dimensional gust applied.")  
    
    # Time series allocation
    Time = np.arange(0,TimeEnd+TimeStep,TimeStep)
    
    print(" Creating gust response for wind speed.")
    Speed = gust_shapes.gust_creator(Time,GustSpeedStart,GustSpeedAmplitude,GustSpeedStartTime,GustSpeedEndTime,GustTypeSpeed)
    
    print(" Creating gust response for wind direction.")
    Direction = gust_shapes.gust_creator(Time,GustDirStart,GustDirAmplitude,GustDirStartTime,GustDirEndTime,GustTypeDir)
    
    
    print(" Adding smoothing regime toward the end of wind file.")
    Time_Smoothed,Vel_x_Smoothed,Vel_y_Smoothed = gust_shapes.adding_linear_smooth_time_vector(Time,TimeSmooth,TimeStep,Speed,Direction)
    Vel_z_Smoothed = np.zeros(len(Time_Smoothed))
    
    
    print(" Recalculating wind speed and direction due to smoothing effect.")
    Speed_Smoothed = np.sqrt(Vel_x_Smoothed**2 + Vel_y_Smoothed**2 + Vel_z_Smoothed**2)
    Direction_Smoothed = np.arctan2(Vel_y_Smoothed,Vel_x_Smoothed) * 180 / np.pi
    
    
    # Collect grid properties with smoothing
    grid_properties = wind_file_creator.collect_grid_info(LogFilePath,Ly,Lz,dy,dz,Time_Smoothed[-1],TimeStep,GustSpeedStart,"LOG")
    dx,dy,dz,num_x,num_y,num_z = grid_properties
    
    
    print(" Expand data in 3D space.")  
    u_array = np.ones(((num_x,num_y,num_z)))
    v_array = np.ones(((num_x,num_y,num_z)))
    w_array = np.ones(((num_x,num_y,num_z)))
    Speed_array = np.ones(((num_x,num_y,num_z)))
    Direction_array = np.ones(((num_x,num_y,num_z)))
    

    for k in range(0,num_z): 
        for j in range(0,num_y): 
            u_array[:,j,k] = Vel_x_Smoothed
            v_array[:,j,k] = Vel_y_Smoothed
            w_array[:,j,k] = Vel_z_Smoothed
            Speed_array[:,j,k] = Speed_Smoothed
            Direction_array[:,j,k] = Direction_Smoothed
            
            
    print(" Plot gust responses at various random locations.")
    gust_plots.plot_gust_signals(Output_Directory_Path,Time_Smoothed,Speed_array,Direction_array,u_array,v_array,
                                 GustSpeedStartTime,GustSpeedEndTime,GustDirStartTime,GustDirEndTime)


        
    
    with open(LogFilePath, 'a') as the_file:
            the_file.write('  \n')
            the_file.write(' ---------------------------- \n')
            the_file.write(' GUST INFORMATION\n')
            the_file.write(' ---------------------------- \n')
            the_file.write(' Target wind file end time: ' + str(Time[-1]) +' s\n')
            the_file.write(' Smoothing time at end of wind file: ' + str(TimeSmooth) +' s\n')
            the_file.write(' Total resulting end time of wind file: ' + str(Time_Smoothed[-1]) +' s\n')
            the_file.write('  \n')
            the_file.write(' Gust dimensionality type: 1-Dimensional\n')
            the_file.write('  \n')
            the_file.write(' Gust type wind speed: ' + str(GustTypeSpeed) +'\n')
            the_file.write(' Gust start time wind speed: ' + str(GustSpeedStartTime) +' s\n')
            the_file.write(' Gust end time wind speed: ' + str(GustSpeedEndTime) +' s\n')    
            the_file.write(' Gust start magnitude wind speed: ' + str(GustSpeedStart) +' m\n')
            the_file.write(' Gust amplitude wind speed: ' + str(GustSpeedAmplitude) +' m\n')
            the_file.write('  \n')
            the_file.write(' Gust type wind direction: ' + str(GustTypeDir) +'\n')
            the_file.write(' Gust start time wind direction: ' + str(GustDirStartTime) +' s\n')
            the_file.write(' Gust end time wind direction: ' + str(GustDirEndTime) +' s\n')    
            the_file.write(' Gust start magnitude wind direction: ' + str(GustDirStart) +' deg\n')
            the_file.write(' Gust amplitude wind direction: ' + str(GustDirAmplitude) +' deg\n')

            
 
    return Time_Smoothed,Speed_array,Direction_array,u_array,v_array,w_array,grid_properties
