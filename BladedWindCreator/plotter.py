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

import os
import numpy as np
import matplotlib.pyplot as plt

################ styling #################
plt.rc('font', family='serif')
plt.rc('font', size=16)


##############################################

def calculate_y_limit(Variable,RatioAdd):
    
    val_min = np.min(Variable)
    val_max = np.max(Variable)
    
    lim1 = val_min - RatioAdd*(val_max-val_min)
    lim2 = val_max + RatioAdd*(val_max-val_min)
    
    return lim1,lim2
    
    
def fill_the_gust_area_function(GustSpeedStartTime,GustSpeedEndTime,GustDirStartTime,GustDirEndTime,y_lim_1,y_lim_2):
    
    x_fill_1 = min(GustSpeedStartTime,GustDirStartTime)
    x_fill_2 = max(GustSpeedEndTime,GustDirEndTime)
    
    y_func = np.linspace(y_lim_1,y_lim_2,5)

    return y_func,x_fill_1,x_fill_2
    

def plot_wind_signal(Output_Directory_Path,Time,Speed,Direction,Vel_x,Vel_y,GustSpeedStartTime,GustSpeedEndTime,GustDirStartTime,GustDirEndTime):

    plt.figure(figsize=(2*7, 3*3))
    
    ax = plt.subplot(3,2,1)
    Variable = Speed * 1.0
    ax.plot(Time,Variable,linestyle="-", markersize=3, color="black", linewidth=1)
    y_lim_1,y_lim_2 = calculate_y_limit(Variable,0.2)
    y_func,x_fill_1,x_fill_2 = fill_the_gust_area_function(GustSpeedStartTime,GustSpeedEndTime,GustDirStartTime,GustDirEndTime,y_lim_1,y_lim_2)
    ax.fill_betweenx(y_func,x_fill_1,x_fill_2, alpha=0.3, color='cyan')
    ax.set_xlim(0,Time[-1])
    ax.set_ylim(y_lim_1,y_lim_2)
    ax.set_xlabel(r'Time [s]')
    ax.set_ylabel(r'$U_\infty$ [m/s]')
    plt.tight_layout()
    
    
    ax = plt.subplot(3,2,2)
    Variable = Direction * 1.0
    ax.plot(Time,Variable,linestyle="-", markersize=3, color="black", linewidth=1)
    y_lim_1,y_lim_2 = calculate_y_limit(Variable,0.2)
    y_func,x_fill_1,x_fill_2 = fill_the_gust_area_function(GustSpeedStartTime,GustSpeedEndTime,GustDirStartTime,GustDirEndTime,y_lim_1,y_lim_2)
    ax.fill_betweenx(y_func,x_fill_1,x_fill_2, alpha=0.3, color='cyan')
    ax.set_xlim(0,Time[-1])
    ax.set_ylim(y_lim_1,y_lim_2)
    ax.set_xlabel(r'Time [s]')
    ax.set_ylabel(r'$\phi$ [deg]')
    plt.tight_layout()
    
    
    
    ax = plt.subplot(3,2,3)
    Variable = Vel_x * 1.0
    ax.plot(Time,Variable,linestyle="-", markersize=3, color="black", linewidth=1)
    y_lim_1,y_lim_2 = calculate_y_limit(Variable,0.2)
    y_func,x_fill_1,x_fill_2 = fill_the_gust_area_function(GustSpeedStartTime,GustSpeedEndTime,GustDirStartTime,GustDirEndTime,y_lim_1,y_lim_2)
    ax.fill_betweenx(y_func,x_fill_1,x_fill_2, alpha=0.3, color='cyan')
    ax.set_xlim(0,Time[-1])
    ax.set_ylim(y_lim_1,y_lim_2)
    ax.set_xlabel(r'Time [s]')
    ax.set_ylabel(r'$v_x$ [m/s]')
    plt.tight_layout()
    
    
    ax = plt.subplot(3,2,4)
    Variable = Vel_y * 1.0
    ax.plot(Time,Variable,linestyle="-", markersize=3, color="black", linewidth=1)
    y_lim_1,y_lim_2 = calculate_y_limit(Variable,0.2)
    y_func,x_fill_1,x_fill_2 = fill_the_gust_area_function(GustSpeedStartTime,GustSpeedEndTime,GustDirStartTime,GustDirEndTime,y_lim_1,y_lim_2)
    ax.fill_betweenx(y_func,x_fill_1,x_fill_2, alpha=0.3, color='cyan')
    ax.set_xlim(0,Time[-1])
    ax.set_ylim(y_lim_1,y_lim_2)
    ax.set_xlabel(r'Time [s]')
    ax.set_ylabel(r'$v_y$ [m/s]')
    plt.tight_layout()
    
    
    
    plt.savefig(os.path.join(Output_Directory_Path,"Wind_Signal.png"), dpi=300, bbox_inches='tight')