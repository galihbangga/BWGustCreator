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
from .. import plotter

##############################################



def plot_gust_signals(Output_Directory_Path,Time,Speed_array,Direction_array,u_array,v_array,
                      GustSpeedStartTime,GustSpeedEndTime,GustDirStartTime,GustDirEndTime):
    '''
    Plot the wind signals at three representative locations of the wind grid:
    center, and 25% and 75% of the grid size in both lateral and vertical directions.

    Output_Directory_Path : directory where the figures are saved
    Time                  : 1D array of time [s], size (nt,)
    Speed_array           : 3D array of wind speed magnitude [m/s], shape (nt, ny, nz)
    Direction_array       : 3D array of wind direction [deg], shape (nt, ny, nz)
    u_array, v_array      : 3D arrays of longitudinal and lateral velocity [m/s], shape (nt, ny, nz)
    GustSpeedStartTime    : start time [s] of the wind speed gust
    GustSpeedEndTime      : end time [s] of the wind speed gust
    GustDirStartTime      : start time [s] of the wind direction gust
    GustDirEndTime        : end time [s] of the wind direction gust
    '''

    num_y,num_z = u_array.shape[1:]

    Locations = [("Wind_Signal_Loc1_Center.png",0.5),
                 ("Wind_Signal_Loc2_2525.png",0.25),
                 ("Wind_Signal_Loc3_7575.png",0.75)]
    for FigureName,Fraction in Locations:
        idx_j = int(Fraction*num_y)
        idx_k = int(Fraction*num_z)
        plotter.plot_wind_signal(Output_Directory_Path,FigureName,Time,
                                 Speed_array[:,idx_j,idx_k],Direction_array[:,idx_j,idx_k],u_array[:,idx_j,idx_k],v_array[:,idx_j,idx_k],
                                 GustSpeedStartTime,GustSpeedEndTime,GustDirStartTime,GustDirEndTime)



def plot_gust_contours_2D(Output_Directory_Path,Time,u_array,v_array,grid_properties,HubHeight,NominalRotorDiameter,
                          GustSpeedStartTime,GustSpeedEndTime):
    '''
    Plot the 2D contours of the wind field in the Y-Z plane at the start, quarter, mid,
    three-quarter and end time of the speed gust, using a common color scale.

    Output_Directory_Path : directory where the figures are saved
    Time                  : 1D array of time [s], size (nt,)
    u_array, v_array      : 3D arrays of longitudinal and lateral velocity [m/s], shape (nt, ny, nz)
    grid_properties       : tuple (dx,dy,dz,num_x,num_y,num_z) describing the wind grid
    HubHeight             : hub height [m], used to reference the grid to absolute height
    NominalRotorDiameter  : rotor diameter [m], drawn as a reference circle
    GustSpeedStartTime    : start time [s] of the wind speed gust
    GustSpeedEndTime      : end time [s] of the wind speed gust
    '''

    dx,dy,dz,num_x,num_y,num_z = grid_properties

    Y_grid = (np.arange(num_y) - 0.5*(num_y-1)) * dy
    Z_grid = (np.arange(num_z) - 0.5*(num_z-1)) * dz + HubHeight
    ContourLimit = max(np.max(np.abs(u_array)), np.max(np.abs(v_array)), 1.0)
    ContourLimits = (-ContourLimit, ContourLimit)

    Contours = [("Wind_Contour_2D_Start.png","start",0.0),
                ("Wind_Contour_2D_Quarter.png","quarter",0.25),
                ("Wind_Contour_2D_Mid.png","mid",0.5),
                ("Wind_Contour_2D_ThreeQuarter.png","three-quarter",0.75),
                ("Wind_Contour_2D_End.png","end",1.0)]
    for FigureName,Label,Fraction in Contours:
        print(" Plot 2D contour of the wind field at the gust " + Label + " time.")
        TimeInstance = GustSpeedStartTime + Fraction*(GustSpeedEndTime - GustSpeedStartTime)
        plotter.plot_wind_contour_2d(Output_Directory_Path,FigureName,Time,Y_grid,Z_grid,
                                     np.transpose(u_array,(0,2,1)),np.transpose(v_array,(0,2,1)),TimeInstance,
                                     HubHeight=HubHeight,Radius=NominalRotorDiameter*0.5,
                                     ColorLimits=ContourLimits)
