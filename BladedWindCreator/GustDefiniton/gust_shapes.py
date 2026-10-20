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
                "FULL" - full cosine rise that returns to the mean at End
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
    elif (Type == "FULL"):
        Tc = (End-Start)
        Actuation[i_actuated] = 0.5*Amplitude*(1 - np.cos(2*np.pi*(t_actuated-Start)/Tc))
    elif (Type == "IEC"):
        Tc = End-Start
        Actuation[i_actuated] = -0.37*Amplitude* np.sin(3*np.pi*(t_actuated-Start)/Tc)*(1 - np.cos(2*np.pi*(t_actuated-Start)/Tc))
    else:
        raise TypeError("Gust type " + Type + " not implemented! Available options are: 'HALF', 'FULL' or 'IEC'")
        
    Gust = Mean + Actuation
    
    return Gust    





def adding_linear_smooth_time(Time,TimeSmooth,TimeStep,ValueBaseline):
    '''
    Replace the last TimeSmooth seconds of a signal by a linear ramp so that the final
    value returns to the initial value of the signal (periodicity for the wind file).
    The signal length is unchanged.

    Time          : 1D array of time [s], size (nt,)
    TimeSmooth    : duration [s] of the smoothing ramp at the end of the signal. If 0, nothing is changed.
    TimeStep      : time step [s] of the signal
    ValueBaseline : 1D array of the signal to be smoothed, size (nt,)

    Returns
    Time_Total  : time array [s], same as Time
    Value_Total : signal array, ending at ValueBaseline[0]
    '''

    Time_Total = Time * 1.0
    Value_Total = ValueBaseline * 1.0

    if (TimeSmooth > 0):

        i_start = len(Time) - 1 - int(round(TimeSmooth/TimeStep))
        if (i_start < 0):
            raise Exception("Smoothing time shall not be larger than the wind file duration")

        fraction = (Time[i_start:]-Time[i_start])/(Time[-1]-Time[i_start])
        Value_Total[i_start:] = ValueBaseline[i_start] + (ValueBaseline[0]-ValueBaseline[i_start])*fraction
    
    return Time_Total,Value_Total



def adding_linear_smooth_time_vector(Time,TimeSmooth,TimeStep,Speed,Direction):
    '''
    Smooth the end of a wind vector signal (see adding_linear_smooth_time) given as speed and direction.
    If the speed at the start of the ramp already equals the initial speed, only the direction is ramped
    and the speed is kept constant. Otherwise the velocity components are ramped.

    Time          : 1D array of time [s], size (nt,)
    TimeSmooth    : duration [s] of the smoothing ramp at the end of the signal. If 0, nothing is changed.
    TimeStep      : time step [s] of the signal
    Speed         : 1D array of wind speed [m/s], size (nt,)
    Direction     : 1D array of wind direction [deg], size (nt,)

    Returns
    Time_Total  : time array [s], same as Time
    Vel_x       : smoothed longitudinal velocity [m/s], size (nt,)
    Vel_y       : smoothed lateral velocity [m/s], size (nt,)
    '''

    Time_Total,Direction_Total = adding_linear_smooth_time(Time,TimeSmooth,TimeStep,Direction)
    i_start = len(Time) - 1 - int(round(TimeSmooth/TimeStep))

    if (TimeSmooth > 0 and np.isclose(Speed[i_start],Speed[0])):
        Speed_Total = Speed * 1.0
        Speed_Total[i_start:] = Speed[0]
        Vel_x = Speed_Total * np.cos(Direction_Total*np.pi/180)
        Vel_y = Speed_Total * np.sin(Direction_Total*np.pi/180)
    else:
        Time_Total,Vel_x = adding_linear_smooth_time(Time,TimeSmooth,TimeStep,Speed*np.cos(Direction*np.pi/180))
        Time_Total,Vel_y = adding_linear_smooth_time(Time,TimeSmooth,TimeStep,Speed*np.sin(Direction*np.pi/180))

    return Time_Total,Vel_x,Vel_y
