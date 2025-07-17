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
import matplotlib.pyplot as plt

################ styling #################
plt.rc('font', family='serif')
plt.rc('font', size=16)


##############################################


def plot_wind_signal(Output_Directory_Path,Time,Speed,Direction,Vel_x,Vel_y):

    plt.figure(figsize=(2*7, 3*3))
    
    ax = plt.subplot(3,2,1)
    ax.plot(Time,Speed,linestyle="-", markersize=3, color="black", linewidth=1)
    ax.set_xlim(0,Time[-1])
    ax.set_xlabel(r'Time [s]')
    ax.set_ylabel(r'$U_\infty$ [m/s]')
    plt.tight_layout()
    
    
    ax = plt.subplot(3,2,2)
    ax.plot(Time,Direction,linestyle="-", markersize=3, color="black", linewidth=1)
    ax.set_xlim(0,Time[-1])
    ax.set_xlabel(r'Time [s]')
    ax.set_ylabel(r'$\phi$ [deg]')
    plt.tight_layout()
    
    
    
    ax = plt.subplot(3,2,3)
    ax.plot(Time,Vel_x,linestyle="-", markersize=3, color="black", linewidth=1)
    ax.set_xlim(0,Time[-1])
    ax.set_xlabel(r'Time [s]')
    ax.set_ylabel(r'$v_x$ [m/s]')
    plt.tight_layout()
    
    
    ax = plt.subplot(3,2,4)
    ax.plot(Time,Vel_y,linestyle="-", markersize=3, color="black", linewidth=1)
    ax.set_xlim(0,Time[-1])
    ax.set_xlabel(r'Time [s]')
    ax.set_ylabel(r'$v_y$ [m/s]')
    plt.tight_layout()
    
    
    
    plt.savefig(os.path.join(Output_Directory_Path,"Wind_Signal.png"), dpi=300, bbox_inches='tight')