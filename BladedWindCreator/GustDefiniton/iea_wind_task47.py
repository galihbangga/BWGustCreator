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



def IEAWind_Task47_Model(LogFilePath,Output_Directory_Path,TimeStep,TimeEnd,TimeSmooth,
                             GustSpeedStartTime,GustSpeedEndTime,GustSpeedStart,GustEccentricity,GustCenter_Y,GustCenter_Z,HubHeight,NominalRotorDiameter,
                             GustTypeDir,GustDirStartTime,GustDirEndTime,GustDirStart,GustDirAmplitude,
                             Ly,Lz,dy,dz):
    '''
    Build a 2-dimensional gust, i.e. a localised velocity excess with a radial
    (tanh) spatial shape in the Y-Z plane and a trapezoidal time evolution.

    LogFilePath           : path of the log file, appended with the gust information
    Output_Directory_Path : directory where the figures are saved
    TimeStep              : time step [s] of the wind file
    TimeEnd               : end time [s] of the wind file
    TimeSmooth            : ramp-up/ramp-down duration [s] of the gust in time, also the duration [s]
                            of the linear ramp at the end of the wind file (within TimeEnd).
                            Must be smaller than GustSpeedStartTime.
    GustSpeedStartTime    : time [s] at which the gust reaches its full magnitude
    GustSpeedEndTime      : time [s] at which the gust starts to decay
    GustSpeedStart        : baseline (uniform) wind speed [m/s]
    GustEccentricity      : inverse spatial extent [1/m] of the gust; larger values
                            give a smaller and sharper gust core
    GustCenter_Y          : lateral offset [m] of the gust center from the grid center
    GustCenter_Z          : vertical offset [m] of the gust center from the grid center
    HubHeight             : hub height [m], used to reference the grid to absolute height
    NominalRotorDiameter  : rotor diameter [m], drawn as a reference circle in the contour plot
    GustTypeDir           : gust shape for wind direction ("HALF" or "IEC")
    GustDirStartTime      : start time [s] of the wind direction gust
    GustDirEndTime        : end time [s] of the wind direction gust
    GustDirStart          : baseline wind direction [deg]
    GustDirAmplitude      : wind direction gust amplitude [deg]
    Ly, Lz                : lateral and vertical extent [m] of the wind grid
    dy, dz                : lateral and vertical grid spacing [m]

    Returns
    Time            : 1D array of time [s], size (nt,)
    Speed_array     : 3D array of wind speed magnitude [m/s], shape (nt, ny, nz)
    Direction_array : 3D array of wind direction [deg], shape (nt, ny, nz)
    u_array         : 3D array of longitudinal velocity [m/s], shape (nt, ny, nz)
    v_array         : 3D array of lateral velocity [m/s], shape (nt, ny, nz)
    w_array         : 3D array of vertical velocity [m/s], shape (nt, ny, nz)
    grid_properties : tuple (dx,dy,dz,num_x,num_y,num_z) describing the wind grid
    '''

    print(" Two-dimensional gust applied.")  
    
    # Time series allocation
    Time = np.arange(0,TimeEnd+TimeStep,TimeStep)
    
    # Collect grid properties with smoothing
    grid_properties = wind_file_creator.collect_grid_info(LogFilePath,Ly,Lz,dy,dz,Time[-1],TimeStep,GustSpeedStart,"LOG")
    dx,dy,dz,num_x,num_y,num_z = grid_properties
    
    
    print(" Expand data in 3D space.")  
    u_array = np.ones(((num_x,num_y,num_z)))
    v_array = np.ones(((num_x,num_y,num_z)))
    w_array = np.ones(((num_x,num_y,num_z)))
    Speed_array = np.ones(((num_x,num_y,num_z)))
    Direction_array = np.ones(((num_x,num_y,num_z)))
    
    
    # Gust 2D function
    if (TimeSmooth > GustSpeedStartTime):
        raise Exception("For 2D gust option smoothting time shall be smaller than start time for gust")  

    print(" Creating gust scaling response in time for wind speed.")               
    Gust_Function = np.zeros(len(Time))
    for i in range(0,len(Time)):
        if (Time[i] < (GustSpeedStartTime - TimeSmooth)):
            Gust_Function_i = 0
        if (Time[i] >= (GustSpeedStartTime - TimeSmooth) and Time[i] < GustSpeedStartTime):
            Gust_Function_i = 0 + (Time[i]-(GustSpeedStartTime - TimeSmooth))/TimeSmooth
        if (Time[i] >= GustSpeedStartTime and Time[i] < GustSpeedEndTime):
            Gust_Function_i = 1      
        if (Time[i] >= GustSpeedEndTime and Time[i] < (GustSpeedEndTime + TimeSmooth)):
            Gust_Function_i = 1 + (Time[i]-GustSpeedEndTime)/TimeSmooth*(0-1)
        if (Time[i] >= (GustSpeedEndTime + TimeSmooth)):
            Gust_Function_i = 0
        Gust_Function[i] = Gust_Function_i

    print(" Creating gust response for wind direction.")
    Direction = gust_shapes.gust_creator(Time,GustDirStart,GustDirAmplitude,GustDirStartTime,GustDirEndTime,GustTypeDir)
      
    
    uniform_wind_x = GustSpeedStart*np.ones(len(Time))
    uniform_wind_y = 0*np.ones(len(Time))
    uniform_wind_z = 0*np.ones(len(Time))
     
    print(" Creating gust scaling response in space for wind speed.")  
    ctr_j = 0.5*(num_y-1)
    ctr_k = 0.5*(num_z-1)
    for k in range(0,num_z): 
        for j in range(0,num_y): 
            y_loc = (j - ctr_j) * dy - GustCenter_Y
            z_loc = (k - ctr_k) * dz - GustCenter_Z
            Radius_Loc = np.sqrt(y_loc**2 + z_loc**2)
            Local_Speed = uniform_wind_x + Gust_Function * 5/2 * ( 1 + np.tanh(-2*np.pi*( 2 * Radius_Loc * GustEccentricity - 1 )) )
            Time_Loc,u_array[:,j,k],v_array[:,j,k] = gust_shapes.adding_linear_smooth_time_vector(Time,TimeSmooth,TimeStep,Local_Speed,Direction)
            w_array[:,j,k] = uniform_wind_z
            Speed_array[:,j,k] = np.sqrt(u_array[:,j,k]**2 + v_array[:,j,k]**2 + w_array[:,j,k]**2)
            Direction_array[:,j,k] = np.arctan2(v_array[:,j,k],u_array[:,j,k]) * 180 / np.pi
               
    print(" Plot gust responses at various random locations.")
    gust_plots.plot_gust_signals(Output_Directory_Path,Time,Speed_array,Direction_array,u_array,v_array,
                                 GustSpeedStartTime,GustSpeedEndTime,GustDirStartTime,GustDirEndTime)
    gust_plots.plot_gust_contours_2D(Output_Directory_Path,Time,u_array,v_array,grid_properties,HubHeight,NominalRotorDiameter,
                                     GustSpeedStartTime,GustSpeedEndTime)
    
    
    with open(LogFilePath, 'a') as the_file:
            the_file.write('  \n')
            the_file.write(' ---------------------------- \n')
            the_file.write(' GUST INFORMATION\n')
            the_file.write(' ---------------------------- \n')
            the_file.write(' Target wind file end time: ' + str(Time[-1]) +' s\n')
            the_file.write(' Smoothing time at end of wind file: ' + str(TimeSmooth) +' s\n')
            the_file.write(' Total resulting end time of wind file: ' + str(Time[-1]) +' s\n')
            the_file.write('  \n')
            the_file.write(' Gust dimensionality type: 2-Dimensional\n')
            the_file.write('  \n')
            the_file.write(' Gust start time wind speed: ' + str(GustSpeedStartTime) +' s\n')
            the_file.write(' Gust end time wind speed: ' + str(GustSpeedEndTime) +' s\n')    
            the_file.write(' Gust start magnitude wind speed: ' + str(GustSpeedStart) +' m\n')
            the_file.write(' Gust eccentricity: ' + str(GustEccentricity) +' \n')
            the_file.write(' Gust center Y: ' + str(GustCenter_Y) +' \n')
            the_file.write(' Gust center Z: ' + str(GustCenter_Z) +' \n')
            the_file.write(' \n')
            the_file.write(' Gust type wind direction: ' + str(GustTypeDir) +'\n')
            the_file.write(' Gust start time wind direction: ' + str(GustDirStartTime) +' s\n')
            the_file.write(' Gust end time wind direction: ' + str(GustDirEndTime) +' s\n')
            the_file.write(' Gust start magnitude wind direction: ' + str(GustDirStart) +' deg\n')
            the_file.write(' Gust amplitude wind direction: ' + str(GustDirAmplitude) +' deg\n')
 
    return Time,Speed_array,Direction_array,u_array,v_array,w_array,grid_properties
