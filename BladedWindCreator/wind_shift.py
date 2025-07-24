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

##############################################


def buffer_time(LogFilePath,Time,TowerExtremaLocation,NominalRotorDiameter,Overhang,LateralOffset,Floating,SeaDepth,WindSpeedRef,InitialNacelleAngle,RotorOrientation,OriginOfWindFileStart):
    
    print(' Calculating turbulent file buffer time.    ')
    
    if (Floating == "YES"):
        FloatingModelTrue = 1
    elif (Floating == "NO"):
        FloatingModelTrue = 0
    else:
        raise TypeError("Unrecognized turbine model, set Floating to 'YES' or 'NO'")
            
    eta = NominalRotorDiameter/2 + np.sqrt(Overhang**2 + LateralOffset**2) + 0.5*SeaDepth*FloatingModelTrue
    x_shift = max(abs(TowerExtremaLocation),eta)
    
    t_shift = x_shift/WindSpeedRef
    
    if (OriginOfWindFileStart == "HUB"):
        t_start_origin = Overhang * np.cos(InitialNacelleAngle*np.pi/180)/WindSpeedRef
    elif (OriginOfWindFileStart == "GLOBAL"): 
        t_start_origin = 0.0
    else:
        raise TypeError("OriginOfWindFileStart " + OriginOfWindFileStart + " not implemented! Available options are: 'GLOBAL' or 'HUB'")    

    if (RotorOrientation == "UPWIND"):
        t_start_origin = 1.0 * t_start_origin
    elif (RotorOrientation == "DOWNWIND"): 
        t_start_origin = -1.0 * t_start_origin
    else:
        raise TypeError("RotorOrientation " + RotorOrientation + " not implemented! Available options are: 'UPWIND' or 'DOWNWIND'") 
    
    turbulent_start_time = Time[-1] - t_shift - t_start_origin
    
    
    with open(LogFilePath, 'a') as the_file:
            the_file.write('  \n')
            the_file.write(' ---------------------------- \n')
            the_file.write(' TURBULENT FILE BUFFER TIME IN BLADED\n')
            the_file.write(' ---------------------------- \n')
            the_file.write(' Start time for turbulent wind: ' + str(turbulent_start_time) +' s\n')
            the_file.write(' Origin of wind file: ' + str(OriginOfWindFileStart) +' \n')
            the_file.write(' RotorOrientation: ' + str(RotorOrientation) +' \n')


    