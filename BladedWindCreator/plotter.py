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

    if (val_min != val_max):
        lim1 = val_min - RatioAdd*(val_max-val_min)
        lim2 = val_max + RatioAdd*(val_max-val_min)
    else:
        lim1 = val_min - RatioAdd
        lim2 = val_max + RatioAdd
        
    return lim1,lim2
    
    
def fill_the_gust_area_function(GustSpeedStartTime,GustSpeedEndTime,GustDirStartTime,GustDirEndTime,y_lim_1,y_lim_2):
    
    x_fill_1 = min(GustSpeedStartTime,GustDirStartTime)
    x_fill_2 = max(GustSpeedEndTime,GustDirEndTime)
    
    y_func = np.linspace(y_lim_1,y_lim_2,5)

    return y_func,x_fill_1,x_fill_2
    

def plot_wind_signal(Output_Directory_Path,FigureName,Time,Speed,Direction,Vel_x,Vel_y,GustSpeedStartTime,GustSpeedEndTime,GustDirStartTime,GustDirEndTime):

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
    
    
    
    plt.savefig(os.path.join(Output_Directory_Path,FigureName), dpi=300, bbox_inches='tight')



def plot_wind_contour_2d(Output_Directory_Path,FigureName,Time,Y,Z,Field_x,Field_y,TimeInstance,
                         Labels=(r'$v_x$ [m/s]',r'$v_y$ [m/s]'),NumLevels=41,HubHeight=None,Radius=None):
    '''
    Plot 2D contour of the wind field at a desired time instance.

    Time        : 1D array of time [s], size (nt,)
    Y           : 1D array of lateral grid coordinates [m], size (ny,)
    Z           : 1D array of vertical grid coordinates [m] (absolute height), size (nz,)
    Field_x     : 3D array of longitudinal (or x) velocity, shape (nt, nz, ny)
    Field_y     : 3D array of lateral (or y) velocity, shape (nt, nz, ny). Can be None.
    TimeInstance: desired time [s]; nearest available time step is used
    HubHeight   : optional hub height [m], drawn as a reference line and rotor center
    Radius      : optional rotor radius [m], drawn as a circle centered at (0,HubHeight)
    '''

    Time = np.asarray(Time)
    idx  = int(np.argmin(np.abs(Time - TimeInstance)))

    Yg, Zg = np.meshgrid(np.asarray(Y), np.asarray(Z))

    Fields = [np.asarray(Field_x)[idx]]
    if Field_y is not None:
        Fields.append(np.asarray(Field_y)[idx])

    nplot = len(Fields)
    fig, axes = plt.subplots(1, nplot, figsize=(7*nplot, 6), squeeze=False)

    for i, (Variable, LabelText) in enumerate(zip(Fields, Labels)):
        ax = axes[0, i]

        v_min, v_max = np.min(Variable), np.max(Variable)
        if v_min == v_max:
            v_min, v_max = v_min - 1.0, v_max + 1.0
        levels = np.linspace(v_min, v_max, NumLevels)

        cf = ax.contourf(Yg, Zg, Variable, levels=levels, cmap='jet', extend='both')
        ax.contour(Yg, Zg, Variable, levels=levels[::5], colors='k', linewidths=0.4)
        if HubHeight is not None:
            ax.axhline(HubHeight, color='white', linestyle='--', linewidth=1)
            ax.axvline(0, color='white', linestyle='--', linewidth=1)

        if (Radius is not None) and (HubHeight is not None):
            theta = np.linspace(0, 2*np.pi, 200)
            ax.plot(Radius*np.cos(theta), HubHeight + Radius*np.sin(theta),
                    color='white', linestyle='-', linewidth=2)
            # tower
            ax.plot([0,0],[0,HubHeight], color='white', linestyle='-', linewidth=2)

        cb = fig.colorbar(cf, ax=ax)
        cb.set_label(LabelText)

        ax.set_xlabel(r'$y$ [m]')
        ax.set_ylabel(r'$z$ [m]')
        ax.set_title(r'$t$ = %.2f s' % Time[idx])
        ax.set_aspect('equal', adjustable='box')

    plt.tight_layout()
    plt.savefig(os.path.join(Output_Directory_Path,FigureName), dpi=300, bbox_inches='tight')
    plt.close(fig)