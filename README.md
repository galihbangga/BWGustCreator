# BWGustCreator
A script to create a wind file using a DNV Bladed format (.wnd) that incorporates gust and wind direction change
Users will be able to generate a wind file that simulate three types of gust

 - HALF
 - FULL
 - IEC
 
both for wind speed and wind direction. Usage of the script is without any guarantee.

# Usage

The main code and input definition can be found on main.py. The following parameters define the input file:

TimeEnd: End time of the wind file, set it long enough to cover your simulation\
TimeStep: Time step of the wind file\
GustTypeSpeed: Type of gust for wind speed\
GustSpeedStartTime: Start time of gust for wind speed\
GustSpeedEndTime: End time of gust for wind speed\
GustSpeedStart: Initial value of the wind speed\
GustSpeedAmplitude: Gust amplitude of the wind speed\
GustTypeDir: Type of gust for wind direction\
GustDirStartTime: Start time of gust for wind direction\
GustDirEndTime: End time of gust for wind direction\
GustDirStart: Initial value of the wind direction\
GustDirAmplitude: Gust amplitude of the wind direction\
Ly: Lateral domain size in m\
Lz: Vertical domain size in m\
dy: Lateral grid spacing in m\
dz: Vertical grid spacing in m\
TowerExtremaLocation: Extreme (absolute largest) value of the support structure coordinate, only relevant for jacket model or large support structure\
NominalRotorDiameter: Nominal rotor diameter (un-coned)\
Overhang: Value of rotor overhang\
LateralOffset: Value of rotor lateral offset\
Floating: Is the wind file prepared for floating wind turbine? "YES" or "NO"\
SeaDepth: Sea depth, only relevant for floating model\
OutName: Name of the output file, extension shall be set to .wnd, for example "Wind_ECG_ECG.wnd"\


# Contributing and Bugs
Contributions are welcomed! For bugs, please contact Galih Bangga, galih.bangga@dnv.com.