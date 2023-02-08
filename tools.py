

import random 

from spade.agent import Agent
import numpy as np
from numpy.random import normal
from ast import literal_eval # It is used to convert the string of a List into List, since SPADE only sends strings type /text 
from homeComponents import EV,NIAppliance,homeBattery,PV,NFA,FA
import matplotlib.pyplot as plt
from init import Irradience, Temperature, domain, Ns,pwd,appliances , batteryCharacteristics, EVcharacteristics
from spade.behaviour import OneShotBehaviour
from spade.message import Message


def defer(I):

    J=[0]*len(I)

    s=random.choice(range(5))
    
    for i in range(len(I)):

        if i < s or i> len(I):

            J[i]=0

        else:

            J[i]=I[i-s]

    return J




def saveData(data,path,filename,extension):
    import os


    if not os.path.exists(path):
        os.makedirs(path)
    
    file=filename + '.'+ extension

    with open(os.path.join(path, file), 'w') as fp:
    
        fp.write(str(data))



def importData(path,filename,extension):

    import numpy as np
    from ast import literal_eval
    
    filename=filename + '.'+ extension  #file name 

    f=open(path+'/'+filename,'r') #open the folder in read method ('r'), error if the file does not exist

    dcon=f.read() #save the data in the file in dcon

    f.close() #close the file

    Data=np.array(literal_eval(dcon)) #--------------converts the text into list 

    return Data



import pandas as pd

import numpy as np
from ast import literal_eval


def importxlsvalue(row,column,file):

    df =file

    a=df.iloc[row,column]

    b=(4*np.array(literal_eval(a))).tolist()   # we multiply by 4 because we have a 15 minute time stem (1/4 of hour)


    return b


# -----------------------------------------------------------------------------
#    This function imports all the appliances from the excel file 

# file= df= = pd.read_excel(r'C:\Users\khali\Dropbox\Khalifa Diack\Simulations\MAS LATEST\appliances.xlsx')
def ExcelAppliances(file):

    df=file

    class Appliance:
        
        NFA_List=[]
        FA_List=[]
        k=-1

        for type in df["ApplianceType"].values:

            k=k+1

            if type == "NFA2":

                stdev=((Ns/24)*np.array(literal_eval(df["stdev"].values[k])))

                durations=(Ns/24)*np.array(literal_eval(df["durations"].values[k]))

                startTimes=(Ns/24)*np.array(literal_eval(df["start_times"].values[k]))

                Rate=df["Rate"].values[k]

                start1=normal(startTimes[0],stdev[0])

                start2=normal(startTimes[1],stdev[0])

                duration1=normal(durations[0],stdev[1])

                duration2=normal(durations[1],stdev[1])

                app=NFA((Rate,start1,start1+duration1),(Rate,start2,start2+duration2))

                NFA_List.append(app)


            if type == "NFA1":

                stdev=df["stdev"].values[k]
                
                startTime=normal((Ns/24)*normal(df["start_times"].values[k],stdev))

                duration=(Ns/24)*df["durations"].values[k]

                Rate=df["Rate"].values[k]

                app=NFA((Rate,startTime,startTime+duration))

                NFA_List.append(app)

            if type == "FA":

                stdev=(Ns/24)*np.array(literal_eval(df["stdev"].values[k]))

                duration=(Ns/24)*df["durations"].values[k]

                operationWindow=(Ns/24)*np.array(literal_eval(df["operationwindow"].values[k]))

                startTime=(Ns/24)*df["start_times"].values[k]

                start=normal(startTime,stdev[0])

                duration1=normal(duration,stdev[1])

                Rate=df["Rate"].values[k]

                app=FA(Rate,operationWindow,[start,duration1])

                FA_List.append(app)

    return Appliance





