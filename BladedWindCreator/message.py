##############################################
'''
Script to create a Bladed wind file according to a specific pattern.

Usage of this script is without guarantee that this will work.

(c) Galih Bangga, DNV, July 2025
If Bug is found, please contact galih.bangga@dnv.com    
'''
##############################################


def splash_start():
    print("                                                                                     ")
    print(" ----------------------------------------------------------------------------------- ")     
    print(" ----------------------------------------------------------------------------------- ") 
    print("                                                                                     ")
    print("   ______          _______ _    _  _____ _______ _____                _              ")
    print("  |  _ \ \        / / ____| |  | |/ ____|__   __/ ____|              | |             ")
    print("  | |_) \ \  /\  / / |  __| |  | | (___    | | | |     _ __ ___  __ _| |_ ___  _ __  ")
    print("  |  _ < \ \/  \/ /| | |_ | |  | |\___ \   | | | |    | '__/ _ \/ _` | __/ _ \| '__| ")
    print("  | |_) | \  /\  / | |__| | |__| |____) |  | | | |____| | |  __/ (_| | || (_) | |    ")
    print("  |____/   \/  \/   \_____|\____/|_____/   |_|  \_____|_|  \___|\__,_|\__\___/|_|    ")
    print("                                                                                     ")
    print("                                                                                     ") 
    print(" (c) Galih Bangga, DNV, 2025                                                         ") 
    print("                                                                                     ")
    print(" ----------------------------------------------------------------------------------- ")     
    print(" ----------------------------------------------------------------------------------- ")
    
def splash_end():

    print(" ------------------------------------------------------------------------------------------------------ ")     
    print(" ------------------------------------------------------------------------------------------------------ ")         
    print(" Congratulations!!!")
    print(' Bladed wind file generation has been successful.')
    print(" ------------------------------------------------------------------------------------------------------ ")     
    print(" ------------------------------------------------------------------------------------------------------ ")   
    
def log_excecution_time(LogFilePath,start_execution_time,end_execution_time,execution_time):
    
    print(' Code starts at : ' + str(start_execution_time)                                   )
    print(' Code ends at : ' + str(end_execution_time)                                       )
    print(' Duration of runs : ' + str(execution_time)                                          )    
    
    with open(LogFilePath, 'a') as the_file:
            the_file.write('  \n')
            the_file.write(' ---------------------------- \n')
            the_file.write(' CODE RUN TIME\n')
            the_file.write(' ---------------------------- \n')        
            the_file.write(' Code starts at : ' + str(start_execution_time) +'\n')
            the_file.write(' Code ends at : ' + str(end_execution_time)  +'\n')
            the_file.write(' Duration of runs : ' + str(execution_time) +'\n')
            
            
         