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
import struct

##############################################


def buffer_time(LogFilePath,TimeEnd,TowerExtremaLocation,NominalRotorDiameter,Overhang,LateralOffset,Floating,SeaDepth,WindSpeedRef):
    
    print(' Calculating turbulent file buffer time.    ')
    
    if (Floating == "YES"):
        FloatingModelTrue = 1
    elif (Floating == "NO"):
        FloatingModelTrue = 0
    else:
        raise TypeError("Unrecognized turbine model, set Floating to 'YES' or 'NO'")
            
    eta = NominalRotorDiameter + np.sqrt(Overhang**2 + LateralOffset**2) + 0.5*SeaDepth*FloatingModelTrue
    x_shift = max(abs(TowerExtremaLocation),eta)
    
    t_shift = x_shift/WindSpeedRef
    
    turbulent_start_time = TimeEnd - t_shift
    
    
    with open(LogFilePath, 'a') as the_file:
            the_file.write('  \n')
            the_file.write(' ---------------------------- \n')
            the_file.write(' TURBULENT FILE BUFFER TIME IN BLADED\n')
            the_file.write(' ---------------------------- \n')
            the_file.write(' Start time for turbulent wind: ' + str(turbulent_start_time) +' s\n')


    

def windlistarange(u,v,w):
    # defining function for restructuring wind field from
    # u = [u1,u2,u3,.....], v = [v1,v2,v3,.....], w = [w1,w2,w3,.....] 
    # Vel = [u1,v1,w1, u2,v2,w2, u3,v3,w3, .....]   
    vel = []
    [vel.extend(list(dummy)) for dummy in zip(u,v,w)]
    
    return vel


def collect_grid_info(LogFilePath,Ly,Lz,dy,dz,TimeEnd,TimeStep,RefWindSpeed):
    
    Lx = RefWindSpeed * TimeEnd
    dx = RefWindSpeed * TimeStep
    num_x = int(TimeEnd/TimeStep)
    num_y = int(Ly/dy)
    num_z = int(Lz/dz)
    
    grid_properties = [dx,dy,dz,num_x,num_y,num_z]
    
    
    with open(LogFilePath, 'a') as the_file:
            the_file.write('  \n')
            the_file.write(' ---------------------------- \n')
            the_file.write(' WIND GRID INFORMATION\n')
            the_file.write(' ---------------------------- \n')
            the_file.write(' Domain size in x: ' + str(Lx) +' m\n')
            the_file.write(' Domain size in y: ' + str(Ly) +' m\n')
            the_file.write(' Domain size in z: ' + str(Lz) +' m\n')
            the_file.write(' Spacing in x: ' + str(dx) +' m\n')
            the_file.write(' Spacing in y: ' + str(dy) +' m\n')
            the_file.write(' Spacing in z: ' + str(dz) +' m\n')
    
    return grid_properties


def generate_uniform_bladed_wind(LogFilePath,OutName,grid_properties,Vel_x,Vel_y,Vel_z,WindSpeedRef):
    

    print(' Finalizing. Preparing the generated wind data in Bladed wind format.    ') 
    
    dx,dy,dz,num_x,num_y,num_z = grid_properties


    ###############################################################################
    # Checking and generating the file
    ###############################################################################
    outputfile = open('Output/'+OutName,'wb')

    ###############################################################################
    # Creating the header
    ###############################################################################
    
    # Getting the bytes
    record_1 = struct.pack('h', -99) # standard bladed number
    record_2 = struct.pack('h', 7) # general Kaimann wind data
    n_header = struct.pack('i', 92) # number of header for Kaimann wind data
    n_turb_comp = struct.pack('i', 3) # 3 wind components
    grid_z = struct.pack('f', dz)
    grid_y = struct.pack('f', dy)
    grid_x = struct.pack('f', dx)
    half_n_gridx = struct.pack('i', int(num_x*0.5)) 
    meanwind = struct.pack('f', WindSpeedRef)
    meanwind = struct.pack('f', WindSpeedRef)
    LScale_uz = struct.pack('f', 10000) # Length scale, fill by any number
    LScale_uy = struct.pack('f', 10000) # Length scale, fill by any number
    LScale_ux = struct.pack('f', 10000) # Length scale, fill by any number
    MaxFreq = struct.pack('f', 10000) # Maximum frequency, for uniform wind fill by any number
    SeedNr = struct.pack('i', 10000) # seed number, for uniform wind fill by any number
    n_gridz = struct.pack('i', num_z)
    n_gridy = struct.pack('i', num_y)
    LScale_vz = struct.pack('f', 10000) # Length scale, fill by any number
    LScale_vy = struct.pack('f', 10000) # Length scale, fill by any number
    LScale_vx = struct.pack('f', 10000) # Length scale, fill by any number
    LScale_wz = struct.pack('f', 10000) # Length scale, fill by any number
    LScale_wy = struct.pack('f', 10000) # Length scale, fill by any number
    LScale_wx = struct.pack('f', 10000) # Length scale, fill by any number
    Kaimal_CohDecay = struct.pack('f', 10000) # Kaimal coherence decay, for uniform wind fill by any number
    Kaimal_CohScale = struct.pack('f', 10000) # Kaimal coherence scale, for uniform wind fill by any number


    # Writing into file
    outputfile.write(record_1)
    outputfile.write(record_2)
    outputfile.write(n_header)
    outputfile.write(n_turb_comp)
    outputfile.write(grid_z)
    outputfile.write(grid_y)
    outputfile.write(grid_x)
    outputfile.write(half_n_gridx)
    outputfile.write(meanwind)
    outputfile.write(LScale_uz)
    outputfile.write(LScale_uy)
    outputfile.write(LScale_ux)
    outputfile.write(MaxFreq)
    outputfile.write(SeedNr)
    outputfile.write(n_gridz)
    outputfile.write(n_gridy)
    outputfile.write(LScale_vz)
    outputfile.write(LScale_vy)
    outputfile.write(LScale_vx)
    outputfile.write(LScale_wz)
    outputfile.write(LScale_wy)
    outputfile.write(LScale_wx)
    outputfile.write(Kaimal_CohDecay)
    outputfile.write(Kaimal_CohScale)

    ###############################################################################
    # Preparing the wind field data 
    ###############################################################################




    ################# set the actual data ######################
    

                    
                    
    endloop = num_x + 1
    for i in range(0,endloop):
        # print ( "idx: " + str(i))
    
        u_t_i = (Vel_x[i]-WindSpeedRef)/WindSpeedRef*1000 # bladed uses integer time 1000 of the float
        v_t_i = Vel_y[i]/WindSpeedRef*1000 # bladed uses integer time 1000 of the float
        w_t_i = Vel_z[i]/WindSpeedRef*1000 # bladed uses integer time 1000 of the float
        
        # print(u_t_i)
        for k in range(0,num_z): 
            
            u_array_t_i_per_row = u_t_i*np.ones(num_y)
            v_array_t_i_per_row = v_t_i*np.ones(num_y)
            w_array_t_i_per_row = w_t_i*np.ones(num_y)

            vel_array_t_i_per_row = windlistarange(u_array_t_i_per_row,v_array_t_i_per_row,w_array_t_i_per_row)
            vel_array_t_i_per_row = np.array(vel_array_t_i_per_row)
            vel_array_t_i_per_row = vel_array_t_i_per_row.astype('int')
           
            
            for n in range(0,len(vel_array_t_i_per_row)):
                
                velfield = struct.pack('h', vel_array_t_i_per_row[n])
                outputfile.write(velfield)
     
    outputfile.close()
    
    
    with open(LogFilePath, 'a') as the_file:
            the_file.write('  \n')
            the_file.write(' ---------------------------- \n')
            the_file.write(' RESCALING WIND IN BLADED\n')
            the_file.write(' ---------------------------- \n')
            the_file.write(' Reference wind speed: ' + str(WindSpeedRef) +' m/s\n')
            the_file.write(' TIx: ' + str(100) +' %\n')
            the_file.write(' TIy: ' + str(100) +' %\n')
            the_file.write(' TIz: ' + str(100) +' %\n')
