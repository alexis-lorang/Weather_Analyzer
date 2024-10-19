############################################################################
# Imports
############################################################################

import time
from time import gmtime, strftime
import Location_Manager
import Clear_Night_Forecast
import Mail_Manager

############################################################################
# Variables
############################################################################

TIME_INTERVALS = 60 # Seconds

############################################################################
# Private Methods
############################################################################


############################################################################
# Public Methods
############################################################################


############################################################################
# Main
############################################################################

# Running the app forever 
while(1):

    Current_Time = strftime("%d-%m - %H:%M", gmtime())

    print(f"{Current_Time} : Start Clear Sky Analyzer")

    Clear_Sky_Flag, Clear_Sky_Date, Clear_Sky_Start, Clear_Sky_Stop = Clear_Night_Forecast.Get_Clear_Sky_Report()

    if Clear_Sky_Flag:

        Mail_Manager.Send_Clear_Sky_Alert(Clear_Sky_Date, Clear_Sky_Start, Clear_Sky_Stop)

    # Waiting TIME_INTERVALS second to run each loop
    time.sleep(TIME_INTERVALS)

    

