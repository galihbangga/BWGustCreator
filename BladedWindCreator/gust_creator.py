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


##############################################


    
def gust_creator(Time,Mean,Amplitude,Start,End,Type):
    
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

def gust_with_wind_direction(LogFilePath,Output_Directory_Path,TimeStep,TimeEnd,TimeSmooth,
                             GustTypeSpeed,GustSpeedStartTime,GustSpeedEndTime,GustSpeedStart,GustSpeedAmplitude,
                             GustTypeDir,GustDirStartTime,GustDirEndTime,GustDirStart,GustDirAmplitude):
    
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
    
    
    print(" Plot gust responses.")
    # Plot results
    plotter.plot_wind_signal(Output_Directory_Path,Time_Smoothed,Speed_Smoothed,Direction_Smoothed,Vel_x_Smoothed,Vel_y_Smoothed,
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

            
 
    return Time_Smoothed,Speed_Smoothed,Direction_Smoothed,Vel_x_Smoothed,Vel_y_Smoothed,Vel_z_Smoothed

        
        
        