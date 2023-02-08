
import numpy as np 
from numpy.random import normal
import statistics as st
import matplotlib.pyplot as plt
from init import Ns, pvCharacteristics, batteryCharacteristics







# In this function we generate 96 values from 24 values of a matrix, to get a 15minutes time- step from a 1 hour time-step 
# We randomly generate 4 values k, l, m and n so that the mean is equal to the value of the vector for 1 hour 
def to15minst(data,error,stdev):
    
    Data=[]
    for i in data:
        mean=0
        k=0
        m=0
        n=0
        l=0
        
        while (mean < i-error or mean>i+error):
            
            k=normal(i,stdev)
            
            l=normal(i,stdev)
            
            m=normal(i,stdev)
            
            n=normal(i,stdev)
            
            mean=st.mean([k,l,m,n])
            
        Data=Data+[abs(k),abs(l),abs(m),abs(n)]
        
    return Data

###################################################################################################################################################

def PV(Irradience, Temperature,numModules):

    Pstc=pvCharacteristics.Pstc #--------------------------------------------------------------------Maximum Power under STC(W)
    NOCT=pvCharacteristics.NOCT #---------------------------------------------------------------------Nominal Operation Cell Temperature (°C)
    Tair_test=pvCharacteristics.Tair_test #-----------------------------------------------------------------the fixed air temperature (°C)
    Tcp=pvCharacteristics.Tcp #-----------------------------------------------------------------Temperature coefficient of Pstc ( W/K)
    Itest=pvCharacteristics.Itest #------------------------------------------------------------------ fixed Irradiation for test (W/m²)
    Tn=pvCharacteristics.Tn #-----------------------------------------------------------------------Nominal temperature (°C)
    

    I=to15minst(Irradience, 0.0001,0)

    Tamb=to15minst(Temperature, 0.0001,0)

    PV_output=[0]*Ns

    Tpv=[0]*Ns

    for i in range(Ns):

        Tpv[i]=Tamb[i]+I[i]*((NOCT-Tair_test)/Itest)#--------------Temperature of the pannel(°C)

        PV_output[i]=numModules*Pstc*I[i]*(1+Tcp*(Tpv[i]-Tn)) #------------------PV generated power (Watts)
    
    return PV_output




###################################################################################################################################################

def NIAppliance(st,et,Rate): # NIAppliance : non interruptible appliance
    #st is the start time, et is the end time and Rate is power consumed in the interval of time
    class NIAppliance():
        pass
    NIAppliance.Rate=Rate
    NIAppliance.st=st
    NIAppliance.et=et
    NIAppliance.Load=[0]*Ns
    for i in range(0,Ns):
        if i<st or i>et:
            NIAppliance.Load[i]=0
        else:
            NIAppliance.Load[i]=Rate
    Load=NIAppliance.Load
    return NIAppliance 

###################################################################################################################################################


class FA: # interruptible appliance



    def __init__(self,Rate,operationWindow,*startANDduration):

        # operationWindow is a list: [start-time ; end time], it is the flexibility interval 

        # operationWindow[0]=predefined start time of the operation window

        # operationWindow[1]=predefined end time of the operation window

        # Rate  is the rated power of the appliance
        
        # *startANDduration are lists [starttime,duration], this appliance is considered as an appliance that operates several times in a day
        # it can start at 8 and finish at 15 then restart at 18 and finish at 22; and so on
        
        

        self.operationWindow=operationWindow
        
        self.consumption=[0]*Ns
        
        self.duration=0 # global duration of the appliance
        
        for i in startANDduration:
            
            self.duration=self.duration+i[1]
            
        
        
        if self.duration > (operationWindow[1]-operationWindow[0]):
            
            print("The required duration doesn't match the operation window")
            
            self.duration=0

        else:
            
            self.duration=self.duration
            
            Load=[]
            g=[]
            for p in startANDduration:
                
                load=[0]*Ns
                k=0
                g.append(p[0])
                for i in range(Ns):
                    
                    if p[0]<=i<p[0]+p[1]:
                        
                        load[i]=Rate
                        
                    else:
                        load[i]=0
                k=k+1
                
                globals()[f"Load{k}"]=load
                
                Load.append(np.array(globals()[f"Load{k}"]))
                    
            self.consumption=sum(Load).tolist()
            self.st=min(g)
                    
        
    


def NFA(*parameters): # NFA : Non flexible appliances with one or multiple operation intarvals in a day (The ' * ' before 'parameters' permits to define unlimited set of parmeters )
     # parameter's syntax for each time interval are (Rated_power, start time, stop time), they can be multiple 
     # if an appliance consumes 7 W from 0 to 10 and 8 W from 11 to Ns, the load is NFA((7,0,10),(8,11,Ns)).
     # parameters are tuples: parameters=(Rated_power, start time, stop time)

                            #          parameters[0]=Rated_power

                            #          parameters[1]=start time

                            #          parameters[2]=stop time
    class NFA():
        pass
    NFA.parameters=parameters
    k=0
    Loads=[]
    for j in NFA.parameters:  # J takes a value of parameters (a set of parameters i.e the value of parameters and parameters=(Rated_power, start time, stop time) ) for each iteration : j[0]=Rated_power, j[1]=start time, j[2]=stop time
        NFA.consumption=[0]*Ns
        for i in range(0,Ns):
            if i<j[1] or i>j[2]: #----------------------- j[1]=start time< i=time step < j[2]=stop time
                NFA.consumption[i]=0
            else:
                NFA.consumption[i]=j[0]
        k=k+1
        globals()[f"Load{k}"]=NFA.consumption
        Loads.append(np.array(globals()[f"Load{k}"]))
    NFA.consumption=sum(Loads).tolist()
    return NFA


###################################################################################################################################################
                
def EV(st,et,Rate,cap,socm,socM):

    # st : start time : the moment when EV began charging
    # et : stop time : the moment when EV stopped charging
    # cap : The capacity the battery (kWh)
    # Rate : Rated charging power
    # socm : Minimum state of charge of the EV battery
    # socM : Maximum state of charge of the EV battery
    
    class EV():
        pass
    soc=[0]*(Ns+1)
    soc[0]=socm
    Cev=[0]*Ns
    Pev=[0]*Ns

    for i in range (0,Ns):

        if i<st or i>et: 
            Cev[i]=0

        elif soc[i]>=socM :
          
            Cev[i]=0
        else:
            Cev[i]=1
        
        Pev[i]= min(Rate,(socM-soc[i])*cap)*Cev[i]
        soc[i+1]=soc[i]+Pev[i]/cap

    EV.soc=soc
    EV.socM=socM
    EV.cap=cap
    EV.Pev=Pev
    EV.Cev=Cev
    return EV


############################################################################################

def homeBattery(numbat,CAP,ps):   
    # cap : The capacity the battery (kWh)
    # ps : Surplus power of the home
    # socm : Minimum state of charge of the battery
    # socM : Maximum state of charge of the battery
    # numbat=1 if the home has a pv system and 0 if not
    
    class homeBattery():
        socm=batteryCharacteristics.socm*numbat
        socM=batteryCharacteristics.socM*numbat
        cap=CAP*1000*(numbat+0.000001e-80)
        soc0=batteryCharacteristics.soc0*numbat
        Pmax=batteryCharacteristics.Pmax*1000*numbat # kw maximum charging and disharging power
        pass
    soc=[0]*(Ns+1)
    soc[0]=homeBattery.soc0
    
    Pch = [0]*Ns #-----------------------Charging power
    Pdis = [0]*Ns #----------------------discharging power
    pdis=[0]*Ns
    for i in range (Ns):
        if ps[i]>=0 :
            Pch[i]= min(ps[i],(homeBattery.socM-soc[i])*homeBattery.cap,homeBattery.Pmax)
            soc[i+1]=soc[i]+Pch[i]/homeBattery.cap
        elif ps[i]<=0 :
            Pdis[i]=max(ps[i],-(soc[i]-homeBattery.socm)*homeBattery.cap,-homeBattery.Pmax)
            soc[i+1]=(soc[i]+Pdis[i]/homeBattery.cap)
            pdis[i]=abs(Pdis[i])
    homeBattery.soc=soc
    homeBattery.initialEnergy=soc[0]*homeBattery.cap
    homeBattery.Pdis=pdis
    homeBattery.Pch=Pch

    return homeBattery

