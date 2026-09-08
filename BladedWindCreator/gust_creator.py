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
from . import plotter
from . import wind_file_creator

##############################################


    
def gust_creator(Time,Mean,Amplitude,Start,End,Type):
    '''
    Create a 1D gust time series superimposed on a constant mean value.

    Time      : 1D array of time [s], size (nt,)
    Mean      : baseline (constant) value of the signal, e.g. wind speed [m/s] or direction [deg]
    Amplitude : gust amplitude, in the same unit as Mean
    Start     : gust start time [s]
    End       : gust end time [s]
    Type      : gust shape, either
                "HALF" - half cosine rise that stays at the elevated level after End
                "IEC"  - IEC extreme operating gust (returns to the mean after End)

    Returns
    Gust      : 1D array of Mean + gust actuation, size (nt,)
    '''

    Actuation = np.zeros(len(Time))
    i_actuated_greater = np.where(Time >= Start)
    i_actuated_smaller = np.where(Time <= End)
    
    i_actuated = np.intersect1d(i_actuated_greater, i_actuated_smaller)
    t_actuated = Time[i_actuated]

    if (Type == "HALF"):
        Tc = 2*(End-Start)
        Actuation[i_actuated] = 0.5*Amplitude*(1 - np.cos(2*np.pi*(t_actuated-Start)/Tc))
        i_actuated_greater_rest = np.where(Time > End)
        Actuation[i_actuated_greater_rest] =  0.5*Amplitude*(1 - np.cos(2*np.pi*(End-Start)/Tc))
    elif (Type == "IEC"):
        Tc = End-Start
        Actuation[i_actuated] = -0.37*Amplitude* np.sin(3*np.pi*(t_actuated-Start)/Tc)*(1 - np.cos(2*np.pi*(t_actuated-Start)/Tc))
    else:
        raise TypeError("Gust type " + Type + " not implemented! Available options are: 'HALF', 'FULL' or 'IEC'")
        
    Gust = Mean + Actuation
    
    return Gust    





def adding_linear_smooth_time(Time,TimeSmooth,TimeStep,ValueBaseline):
    '''
    Append a linear ramp at the end of a signal so that the final value
    returns to the initial value of the signal (periodicity for the wind file).

    Time          : 1D array of time [s], size (nt,)
    TimeSmooth    : duration [s] of the appended smoothing ramp. If 0, nothing is added.
    TimeStep      : time step [s] used to build the appended time samples
    ValueBaseline : 1D array of the signal to be smoothed, size (nt,)

    Returns
    Time_Total  : extended time array [s]
    Value_Total : extended signal array, ending at ValueBaseline[0]
    '''

    if (TimeSmooth > 0):
    
        Time_Smooth = np.arange(Time[-1]+TimeStep,Time[-1]+TimeSmooth+TimeStep,TimeStep)
        
        gradient = (ValueBaseline[0]-ValueBaseline[-1])/(Time_Smooth[-1]-Time[-1])
        
        ValueSmooth = ValueBaseline[-1] + gradient*(Time_Smooth-Time[-1])
        
        Time_Total = np.append(Time,Time_Smooth)
        Value_Total = np.append(ValueBaseline,ValueSmooth)
    
    else:
        Time_Total = Time * 1.0
        Value_Total = ValueBaseline * 1.0
    
    return Time_Total,Value_Total



def gust_with_wind_direction_1D(LogFilePath,Output_Directory_Path,TimeStep,TimeEnd,TimeSmooth,
                             GustTypeSpeed,GustSpeedStartTime,GustSpeedEndTime,GustSpeedStart,GustSpeedAmplitude,
                             GustTypeDir,GustDirStartTime,GustDirEndTime,GustDirStart,GustDirAmplitude,Ly,Lz,dy,dz):
    '''
    Build a 1-dimensional (uniform over the grid plane) gust in both wind speed and
    wind direction, expand it over the 3D wind grid and generate the diagnostic plots.

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
    Time_Smoothed   : 1D array of time [s] including the smoothing ramp, size (nt,)
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
    Speed = gust_creator(Time,GustSpeedStart,GustSpeedAmplitude,GustSpeedStartTime,GustSpeedEndTime,GustTypeSpeed)
    
    print(" Creating gust response for wind direction.")
    Direction = gust_creator(Time,GustDirStart,GustDirAmplitude,GustDirStartTime,GustDirEndTime,GustTypeDir)
    
    
    print(" Combining wind speed and direction gust responses.")
    Vel_x = Speed * np.cos(Direction*np.pi/180)
    Vel_y = Speed * np.sin(Direction*np.pi/180)
    Vel_z = np.zeros(len(Speed))
    
    
    print(" Adding smoothing regime toward the end of wind file.")
    Time_Smoothed,Vel_x_Smoothed = adding_linear_smooth_time(Time,TimeSmooth,TimeStep,Vel_x)
    Time_Smoothed,Vel_y_Smoothed = adding_linear_smooth_time(Time,TimeSmooth,TimeStep,Vel_y)
    Time_Smoothed,Vel_z_Smoothed = adding_linear_smooth_time(Time,TimeSmooth,TimeStep,Vel_z)
    
    
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
    
    
    
    # Plot results
    FigureName = "Wind_Signal_Loc1_Center.png"
    idx_j = int(0.5*num_y)
    idx_k = int(0.5*num_z)
    Speed_Plot = Speed_array[:,idx_j,idx_k]
    Direction_Plot = Direction_array[:,idx_j,idx_k]
    VelX_Plot = u_array[:,idx_j,idx_k]
    VelY_Plot = v_array[:,idx_j,idx_k]
    plotter.plot_wind_signal(Output_Directory_Path,FigureName,Time_Smoothed,Speed_Plot,Direction_Plot,VelX_Plot,VelY_Plot,
                            GustSpeedStartTime,GustSpeedEndTime,GustDirStartTime,GustDirEndTime)
    
    
    # Plot results
    FigureName = "Wind_Signal_Loc2_2525.png"
    idx_j = int(0.25*num_y)
    idx_k = int(0.25*num_z)
    Speed_Plot = Speed_array[:,idx_j,idx_k]
    Direction_Plot = Direction_array[:,idx_j,idx_k]
    VelX_Plot = u_array[:,idx_j,idx_k]
    VelY_Plot = v_array[:,idx_j,idx_k]
    plotter.plot_wind_signal(Output_Directory_Path,FigureName,Time_Smoothed,Speed_Plot,Direction_Plot,VelX_Plot,VelY_Plot,
                            GustSpeedStartTime,GustSpeedEndTime,GustDirStartTime,GustDirEndTime) 
    
    
    # Plot results
    FigureName = "Wind_Signal_Loc3_7575.png"
    idx_j = int(0.75*num_y)
    idx_k = int(0.75*num_z)
    Speed_Plot = Speed_array[:,idx_j,idx_k]
    Direction_Plot = Direction_array[:,idx_j,idx_k]
    VelX_Plot = u_array[:,idx_j,idx_k]
    VelY_Plot = v_array[:,idx_j,idx_k]
    plotter.plot_wind_signal(Output_Directory_Path,FigureName,Time_Smoothed,Speed_Plot,Direction_Plot,VelX_Plot,VelY_Plot,
                            GustSpeedStartTime,GustSpeedEndTime,GustDirStartTime,GustDirEndTime) 


        
    
    with open(LogFilePath, 'a') as the_file:
            the_file.write('  \n')
            the_file.write(' ---------------------------- \n')
            the_file.write(' GUST INFORMATION\n')
            the_file.write(' ---------------------------- \n')
            the_file.write(' Target wind file end time: ' + str(Time[-1]) +' s\n')
            the_file.write(' Additional smoothing time: ' + str(Time_Smoothed[-1]-Time[-1]) +' s\n')
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

        
        
        
        
def gust_with_wind_direction_2D(LogFilePath,Output_Directory_Path,TimeStep,TimeEnd,TimeSmooth,
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
    TimeSmooth            : ramp-up/ramp-down duration [s] of the gust in time.
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
    Direction = gust_creator(Time,GustDirStart,GustDirAmplitude,GustDirStartTime,GustDirEndTime,GustTypeDir)
    Direction_Radians = Direction*np.pi/180
      
    
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
            u_array[:,j,k] = Local_Speed * np.cos(Direction_Radians)
            v_array[:,j,k] = Local_Speed * np.sin(Direction_Radians)
            w_array[:,j,k] = uniform_wind_z
            Speed_array[:,j,k] = np.sqrt(u_array[:,j,k]**2 + v_array[:,j,k]**2 + w_array[:,j,k]**2)
            Direction_array[:,j,k] = np.arctan2(v_array[:,j,k],u_array[:,j,k]) * 180 / np.pi
               
    print(" Plot gust responses at various random locations.")
    
    # Plot results
    FigureName = "Wind_Signal_Loc1_Center.png"
    idx_j = int(0.5*num_y)
    idx_k = int(0.5*num_z)
    Speed_Plot = Speed_array[:,idx_j,idx_k]
    Direction_Plot = Direction_array[:,idx_j,idx_k]
    VelX_Plot = u_array[:,idx_j,idx_k]
    VelY_Plot = v_array[:,idx_j,idx_k]
    plotter.plot_wind_signal(Output_Directory_Path,FigureName,Time,Speed_Plot,Direction_Plot,VelX_Plot,VelY_Plot,
                            GustSpeedStartTime,GustSpeedEndTime,GustDirStartTime,GustDirEndTime)
    
    
    # Plot results
    FigureName = "Wind_Signal_Loc2_2525.png"
    idx_j = int(0.25*num_y)
    idx_k = int(0.25*num_z)
    Speed_Plot = Speed_array[:,idx_j,idx_k]
    Direction_Plot = Direction_array[:,idx_j,idx_k]
    VelX_Plot = u_array[:,idx_j,idx_k]
    VelY_Plot = v_array[:,idx_j,idx_k]
    plotter.plot_wind_signal(Output_Directory_Path,FigureName,Time,Speed_Plot,Direction_Plot,VelX_Plot,VelY_Plot,
                            GustSpeedStartTime,GustSpeedEndTime,GustDirStartTime,GustDirEndTime) 
    
    
    # Plot results
    FigureName = "Wind_Signal_Loc3_7575.png"
    idx_j = int(0.75*num_y)
    idx_k = int(0.75*num_z)
    Speed_Plot = Speed_array[:,idx_j,idx_k]
    Direction_Plot = Direction_array[:,idx_j,idx_k]
    VelX_Plot = u_array[:,idx_j,idx_k]
    VelY_Plot = v_array[:,idx_j,idx_k]
    plotter.plot_wind_signal(Output_Directory_Path,FigureName,Time,Speed_Plot,Direction_Plot,VelX_Plot,VelY_Plot,
                            GustSpeedStartTime,GustSpeedEndTime,GustDirStartTime,GustDirEndTime) 
        
    
    print(" Plot 2D contour of the wind field at the gust start time.")
    Y_grid = (np.arange(num_y) - ctr_j) * dy
    Z_grid = (np.arange(num_z) - ctr_k) * dz + HubHeight
    TimeInstance = GustSpeedStartTime + 0.0*(GustSpeedEndTime - GustSpeedStartTime)
    ContourLimit = max(np.max(np.abs(u_array)), np.max(np.abs(v_array)), 1.0)
    ContourLimits = (-ContourLimit, ContourLimit)
    plotter.plot_wind_contour_2d(Output_Directory_Path,"Wind_Contour_2D_Start.png",Time,Y_grid,Z_grid,
                                 np.transpose(u_array,(0,2,1)),np.transpose(v_array,(0,2,1)),TimeInstance,
                                 HubHeight=HubHeight,Radius=NominalRotorDiameter*0.5,
                                 ColorLimits=ContourLimits)
    
    
    print(" Plot 2D contour of the wind field at the gust quarter time.")
    Y_grid = (np.arange(num_y) - ctr_j) * dy
    Z_grid = (np.arange(num_z) - ctr_k) * dz + HubHeight
    TimeInstance = GustSpeedStartTime + 0.25*(GustSpeedEndTime - GustSpeedStartTime)
    ContourLimit = max(np.max(np.abs(u_array)), np.max(np.abs(v_array)), 1.0)
    ContourLimits = (-ContourLimit, ContourLimit)
    plotter.plot_wind_contour_2d(Output_Directory_Path,"Wind_Contour_2D_Quarter.png",Time,Y_grid,Z_grid,
                                 np.transpose(u_array,(0,2,1)),np.transpose(v_array,(0,2,1)),TimeInstance,
                                 HubHeight=HubHeight,Radius=NominalRotorDiameter*0.5,
                                 ColorLimits=ContourLimits)    
    
        
    print(" Plot 2D contour of the wind field at the gust mid time.")
    Y_grid = (np.arange(num_y) - ctr_j) * dy
    Z_grid = (np.arange(num_z) - ctr_k) * dz + HubHeight
    TimeInstance = 0.5*(GustSpeedStartTime + GustSpeedEndTime)
    plotter.plot_wind_contour_2d(Output_Directory_Path,"Wind_Contour_2D_Mid.png",Time,Y_grid,Z_grid,
                                 np.transpose(u_array,(0,2,1)),np.transpose(v_array,(0,2,1)),TimeInstance,
                                 HubHeight=HubHeight,Radius=NominalRotorDiameter*0.5,
                                 ColorLimits=ContourLimits)


    print(" Plot 2D contour of the wind field at the gust three-quarter time.")
    Y_grid = (np.arange(num_y) - ctr_j) * dy
    Z_grid = (np.arange(num_z) - ctr_k) * dz + HubHeight
    TimeInstance = GustSpeedStartTime + 0.75*(GustSpeedEndTime - GustSpeedStartTime)
    ContourLimit = max(np.max(np.abs(u_array)), np.max(np.abs(v_array)), 1.0)
    ContourLimits = (-ContourLimit, ContourLimit)
    plotter.plot_wind_contour_2d(Output_Directory_Path,"Wind_Contour_2D_ThreeQuarter.png",Time,Y_grid,Z_grid,
                                 np.transpose(u_array,(0,2,1)),np.transpose(v_array,(0,2,1)),TimeInstance,
                                 HubHeight=HubHeight,Radius=NominalRotorDiameter*0.5,
                                 ColorLimits=ContourLimits) 


    print(" Plot 2D contour of the wind field at the gust end time.")
    Y_grid = (np.arange(num_y) - ctr_j) * dy
    Z_grid = (np.arange(num_z) - ctr_k) * dz + HubHeight
    TimeInstance = GustSpeedStartTime + 1.0*(GustSpeedEndTime - GustSpeedStartTime)
    plotter.plot_wind_contour_2d(Output_Directory_Path,"Wind_Contour_2D_End.png",Time,Y_grid,Z_grid,
                                 np.transpose(u_array,(0,2,1)),np.transpose(v_array,(0,2,1)),TimeInstance,
                                 HubHeight=HubHeight,Radius=NominalRotorDiameter*0.5,
                                 ColorLimits=ContourLimits)
    
    
    with open(LogFilePath, 'a') as the_file:
            the_file.write('  \n')
            the_file.write(' ---------------------------- \n')
            the_file.write(' GUST INFORMATION\n')
            the_file.write(' ---------------------------- \n')
            the_file.write(' Target wind file end time: ' + str(Time[-1]) +' s\n')
            the_file.write(' Additional smoothing time: ' + str(TimeSmooth) +' s\n')
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
