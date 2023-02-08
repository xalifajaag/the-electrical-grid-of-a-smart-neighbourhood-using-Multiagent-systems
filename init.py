

import sys
import os
import subprocess



#   Uncomment the lines below to automatically install the required modules

# subprocess.check_call([sys.executable, '-m', 'pip', 'install', 
#  'spade','pandas','numpy','matplotlib','openpyxl'])

# os.system('cls')




import pandas as pd



# CONNECTION INFOS--------------------------------------------------

#  FOR THE PUBLIC SERVER MAGIC BROCCOLI -------------------------


# domain="magicbroccoli.de"  # the domain of the XMPP server

# pwd="we&you@utc2022"       # the pass word of homes and the aggregator


#   FOR THE OPENFIRE LOCAL SERVER -------------------------------------

domain="localhost"  # the domain of the XMPP server

pwd="st50"       # the pass word of homes and the aggregator


##########################################################################################

path=r'E:\ST50\PROGRAMS\MAS LATEST\Datas'    # The directory of the simulation files

AggregatorPath=path + r'\aggregator'

HomePath=path + r'\Homes\ '

Ns=96   # number of time steps

class pvCharacteristics:

    Pstc=250 #--------------------------------------------------------------------Maximum Power under STC(W)
    NOCT=48 #---------------------------------------------------------------------Nominal Operation Cell Temperature (°C)
    Tair_test=23#-----------------------------------------------------------------the fixed air temperature (°C)
    Tcp=-0.0043 #-----------------------------------------------------------------Temperature coefficient of Pstc ( W/K)
    Itest=800 #------------------------------------------------------------------ fixed Irradiation for test (W/m²)
    Tn=25 #-----------------------------------------------------------------------Nominal temperature (°C)


Irradience=[0,0,0,0,0.065,0.174,0.259,0.306,0.343,0.356,0.357,0.363,0.355,0.339,0.327,0.312,0.276,0.229,0.145,0.017,0,0,0,0] # Irradiation W/m²

Temperature=[12,11,11,10,8,9,8,10,12,13,14,17,18,19,20,21,20,21,20,20,19,18,17,16] #--------------------Temperature (°C)



######################################################################################################################################################
#                 Appliance simulation data

appliances = pd.read_excel(r'C:\Users\khali\Dropbox\Khalifa Diack\Simulations\MAS LATEST\appliances.xlsx')

# HOME BAttery--------------------------------------------------------------------------------------------------
class batteryCharacteristics:
    cap=100 # kWh
    soc0=0.15 # initial state of charge 
    socm=0.1 # minimal soc
    socM=0.95 # maximal soc
    Pmax=5 # kw maximum charging and disharging power
    # efficiency=0.95 # Efficiency off the battery


# EV characteristics ********************************************************************************************


class EVcharacteristics:
    
    st=4 # : start time : the moment when EV began charging
    et= 80 # : stop time : the moment when EV stopped charging
    cap=40*1000 # : The capacity the battery (Wh)
    Rate=1200 # : Rated charging power (W)
    socm = 0.15 #: Minimum state of charge of the EV battery
    socM=0.95    # : Maximum state of charge of the EV battery
    soc0=0.16    # initial soc
    
