# download_dmi_weather_archive

Downloads data from DMI's weather archive. In this example, windspeed and direction is downloaded for multiple stations and stored locally in .csv files.

https://www.dmi.dk/vejrarkiv/

To change any parameter look into the request URL:

https://www.dmi.dk/dmidk_obsWS/rest/archive/hourly/danmark/wind/Aalborg/2018/Marts/25  // Wind [m/s]
https://www.dmi.dk/dmidk_obsWS/rest/archive/hourly/danmark/winddir/Aalborg/2018/Marts/29 // Wind direction [degrees]

The parameters "wind" and "windir" can be changed to
one of the following standard parameters:

"temperature", "precip", "pressure", "humidity",
"wind", and "windir".

However, playing around with undocumented common variables,
e.g. "radiation" will also return valid data.

If modified or used in any projects, please
refer to the author.

LEGAL DISCLAIMER:

This script is for educational use and the 
original author does not take responsibility 
for any illegal use of this script. You shall 
not use this script for any illegal purposes!
