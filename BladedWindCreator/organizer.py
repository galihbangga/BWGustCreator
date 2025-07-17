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
import shutil

##############################################


def create_output_directory():
    
    print(" Creating output directory. Old output directory/results will be removed!")
    
    Output_Directory_Path = os.path.join(os.getcwd(),"Output")
    
    # Check the results directory, delete if it exist before running to ensure always latest
    if os.path.isdir(Output_Directory_Path):
                shutil.rmtree(Output_Directory_Path)
    
    # recreate output directory
    if (os.path.isdir(Output_Directory_Path) ==  False):
        os.mkdir(Output_Directory_Path)
        
        # Defining Output Log
        LogFilePath = os.path.join(Output_Directory_Path,'WindFileCreatorLog.dat')
        with open(LogFilePath, 'a') as the_file:
                the_file.write("  \n")
                the_file.write(" -----------------------------------------------------------------------------------  \n")
                the_file.write(" -----------------------------------------------------------------------------------  \n")
                the_file.write("   ______          _______ _    _  _____ _______ _____                _               \n")
                the_file.write("  |  _ \ \        / / ____| |  | |/ ____|__   __/ ____|              | |              \n")
                the_file.write("  | |_) \ \  /\  / / |  __| |  | | (___    | | | |     _ __ ___  __ _| |_ ___  _ __   \n")
                the_file.write("  |  _ < \ \/  \/ /| | |_ | |  | |\___ \   | | | |    | '__/ _ \/ _` | __/ _ \| '__|  \n")
                the_file.write("  | |_) | \  /\  / | |__| | |__| |____) |  | | | |____| | |  __/ (_| | || (_) | |     \n")
                the_file.write("  |____/   \/  \/   \_____|\____/|_____/   |_|  \_____|_|  \___|\__,_|\__\___/|_|     \n")
                the_file.write("                                                                                      \n")
                the_file.write(" -----------------------------------------------------------------------------------  \n")
                the_file.write(" -----------------------------------------------------------------------------------  \n")

            
            
    return Output_Directory_Path,LogFilePath